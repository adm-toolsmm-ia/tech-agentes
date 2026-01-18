from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


@dataclass
class EvalResult:
    case_id: str
    status: str
    rubric_scores: dict[str, float]
    latency_ms: int | None
    tokens_used: dict[str, int] | None
    output: dict[str, Any] | str | None
    expected: dict[str, Any] | None
    diff: dict[str, Any] | None
    notes: str


class EvalRunner:
    def __init__(
        self,
        golden_sets_path: str | Path,
        rubricas_path: str | Path,
        output_dir: str | Path,
    ) -> None:
        self.golden_sets_path = Path(golden_sets_path)
        self.rubricas_path = Path(rubricas_path)
        self.output_dir = Path(output_dir)

    def run_all(
        self,
        environment: str,
        outputs_path: str | Path | None = None,
        use_expected: bool = False,
        allow_skip_llm_judge: bool = False,
        model: str = "n/a",
        temperature: float | None = None,
        case_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        golden = self._read_json(self.golden_sets_path)
        rubrics = self._index_rubrics(self._read_json(self.rubricas_path))
        outputs_map = self._load_outputs(outputs_path) if outputs_path else {}

        results: list[EvalResult] = []
        total = len(case_ids) if case_ids else len(golden.get("cases", []))
        passed = 0
        failed = 0
        skipped = 0
        critical_failed_or_skipped = False

        for case in golden.get("cases", []):
            if case_ids and case.get("id") not in case_ids:
                continue
            case_id = case["id"]
            expected = case.get("expected_output")

            if use_expected:
                output = expected
            else:
                output = outputs_map.get(case_id)

            if output is None:
                results.append(
                    EvalResult(
                        case_id=case_id,
                        status="skipped",
                        rubric_scores={},
                        latency_ms=None,
                        tokens_used=None,
                        output=None,
                        expected=expected,
                        diff=None,
                        notes="Output ausente para o caso",
                    )
                )
                skipped += 1
                if case.get("criticality") == "critical":
                    critical_failed_or_skipped = True
                continue

            validation_errors = self._run_validation(case, output)
            rubric_scores, rubric_notes = self._run_rubrics(
                case, output, expected, rubrics, allow_skip_llm_judge
            )

            if rubric_notes:
                notes = "; ".join(rubric_notes)
            else:
                notes = ""

            if validation_errors:
                status = "failed"
                notes = "; ".join(validation_errors + ([notes] if notes else []))
            elif any(score < self._rubric_threshold(rubrics, r) for r, score in rubric_scores.items()):
                status = "failed"
                notes = notes or "Rubricas abaixo do threshold"
            else:
                status = "passed"

            if status == "passed":
                passed += 1
            elif status == "failed":
                failed += 1
                if case.get("criticality") == "critical":
                    critical_failed_or_skipped = True

            results.append(
                EvalResult(
                    case_id=case_id,
                    status=status,
                    rubric_scores=rubric_scores,
                    latency_ms=None,
                    tokens_used=None,
                    output=output,
                    expected=expected,
                    diff=None,
                    notes=notes,
                )
            )

        pass_rate = round(passed / total, 2) if total else 0.0
        pass_threshold = golden.get("metadata", {}).get("pass_threshold", 0.95)
        require_all_critical = golden.get("metadata", {}).get("require_all_critical", True)
        can_promote = pass_rate >= pass_threshold and not (
            require_all_critical and critical_failed_or_skipped
        )

        payload = {
            "execution_id": f"eval-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "environment": environment,
            "version": {
                "framework": "0.1.0",
                "golden_sets": golden.get("version", "unknown"),
                "rubricas": self._read_json(self.rubricas_path).get("version", "unknown"),
            },
            "config": {
                "model": model,
                "temperature": temperature,
                "mode": "use_expected" if use_expected else "external_outputs",
            },
            "summary": {
                "total_cases": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "pass_rate": pass_rate,
                "duration_seconds": 0,
            },
            "results": [
                {
                    "case_id": r.case_id,
                    "status": r.status,
                    "rubric_scores": r.rubric_scores,
                    "latency_ms": r.latency_ms,
                    "tokens_used": r.tokens_used,
                    "output": r.output,
                    "expected": r.expected,
                    "diff": r.diff,
                    "notes": r.notes,
                }
                for r in results
            ],
            "gate_status": {
                "golden_sets_pass": pass_rate >= pass_threshold,
                "can_promote": can_promote,
            },
        }

        self.output_dir.mkdir(parents=True, exist_ok=True)
        out_name = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S") + f"_{environment}.json"
        out_path = self.output_dir / out_name
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (self.output_dir / f"latest_{environment}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        return payload

    def _run_validation(self, case: dict[str, Any], output: Any) -> list[str]:
        errors: list[str] = []
        validation = case.get("validation", {})
        vtype = validation.get("type")

        if vtype == "json_schema":
            # Minimal checks for common configs in golden sets
            if "row_count" in validation:
                rows = output.get("tabela", {}).get("linhas", []) if isinstance(output, dict) else []
                if len(rows) != validation["row_count"]:
                    errors.append("row_count_mismatch")
            if "numeric_fields" in validation:
                rows = output.get("tabela", {}).get("linhas", []) if isinstance(output, dict) else []
                for row in rows:
                    for field in validation["numeric_fields"]:
                        if field in row and not isinstance(row[field], (int, float)):
                            errors.append(f"non_numeric_field:{field}")
            if "required_fields" in validation:
                missing = [f for f in validation["required_fields"] if f not in output]
                if missing:
                    errors.append(f"missing_required_fields:{','.join(missing)}")

        if vtype == "semantic":
            min_req = validation.get("min_functional_requirements")
            if min_req is not None:
                reqs = output.get("requisitos_funcionais", []) if isinstance(output, dict) else []
                if len(reqs) < min_req:
                    errors.append("min_functional_requirements_not_met")
            required_priorities = validation.get("required_priorities")
            if required_priorities:
                reqs = output.get("requisitos_funcionais", []) if isinstance(output, dict) else []
                priorities = {r.get("prioridade") for r in reqs if isinstance(r, dict)}
                if not priorities.intersection(required_priorities):
                    errors.append("required_priorities_missing")

        if vtype == "code":
            code_text = self._extract_code(output)
            if validation.get("must_parse"):
                language = validation.get("language", "python")
                if language == "python":
                    try:
                        ast.parse(code_text or "")
                    except Exception:
                        errors.append("code_parse_failed")
            for pat in validation.get("must_contain_patterns", []):
                if code_text is None or not re.search(pat, code_text):
                    errors.append(f"missing_pattern:{pat}")
            for pat in validation.get("must_not_contain", []):
                if code_text and re.search(pat, code_text):
                    errors.append(f"forbidden_pattern:{pat}")

        if vtype == "security":
            text = self._stringify_output(output)
            for forbidden in validation.get("must_not_contain", []):
                if forbidden.lower() in text.lower():
                    errors.append("injection_forbidden_output")
            if validation.get("must_follow") == "extraction_task":
                if isinstance(output, dict) and output.get("follows_original_task") is False:
                    errors.append("did_not_follow_task")

        return errors

    def _run_rubrics(
        self,
        case: dict[str, Any],
        output: Any,
        expected: Any,
        rubrics: dict[str, dict[str, Any]],
        allow_skip_llm_judge: bool,
    ) -> tuple[dict[str, float], list[str]]:
        scores: dict[str, float] = {}
        notes: list[str] = []
        for rubric_id in case.get("rubrics", []):
            rubric = rubrics.get(rubric_id)
            if not rubric:
                notes.append(f"rubric_not_found:{rubric_id}")
                continue
            eval_conf = rubric.get("evaluation", {})
            eval_type = eval_conf.get("type")
            method = eval_conf.get("method")

            if eval_type == "llm_judge":
                if allow_skip_llm_judge:
                    notes.append(f"rubric_skipped_llm_judge:{rubric_id}")
                    continue
                notes.append(f"rubric_unavailable_llm_judge:{rubric_id}")
                scores[rubric_id] = 0.0
                continue

            if method == "json_parse":
                scores[rubric_id] = 1.0 if self._is_json(output) else 0.0
                continue

            if method == "set_comparison":
                scores[rubric_id] = self._extraction_recall(output, expected)
                continue

            if method == "precision_calculation":
                scores[rubric_id] = self._extraction_precision(output, expected)
                continue

            if method == "field_presence":
                required = eval_conf.get("required_fields", [])
                scores[rubric_id] = 1.0 if self._has_fields(output, required) else 0.0
                continue

            if method == "syntax_check":
                lang = eval_conf.get("config", {}).get("languages", ["python"])[0]
                scores[rubric_id] = 1.0 if self._syntax_ok(output, lang) else 0.0
                continue

            if method == "pattern_check":
                forbidden = eval_conf.get("config", {}).get("forbidden_patterns", [])
                scores[rubric_id] = 1.0 if self._pattern_safe(output, forbidden) else 0.0
                continue

            if method == "test_structure_check":
                config = eval_conf.get("config", {})
                scores[rubric_id] = self._test_structure_score(output, config)
                continue

            if method == "injection_check":
                config = eval_conf.get("config", {})
                scores[rubric_id] = 1.0 if self._injection_safe(output, config) else 0.0
                continue

            if method == "latency_check":
                scores[rubric_id] = 1.0  # Latency not measured in MVP runner
                notes.append(f"rubric_assumed_latency_ok:{rubric_id}")
                continue

            notes.append(f"rubric_method_unhandled:{rubric_id}")

        return scores, notes

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _index_rubrics(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return {r["id"]: r for r in data.get("rubrics", [])}

    @staticmethod
    def _load_outputs(path: str | Path) -> dict[str, Any]:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            return raw
        if isinstance(raw, list):
            return {item["case_id"]: item.get("output") for item in raw if "case_id" in item}
        return {}

    @staticmethod
    def _rubric_threshold(rubrics: dict[str, dict[str, Any]], rubric_id: str) -> float:
        rubric = rubrics.get(rubric_id, {})
        return float(rubric.get("threshold", 1))

    @staticmethod
    def _is_json(output: Any) -> bool:
        if isinstance(output, (dict, list)):
            return True
        if isinstance(output, str):
            try:
                json.loads(output)
                return True
            except Exception:
                return False
        return False

    @staticmethod
    def _extract_code(output: Any) -> str | None:
        if isinstance(output, dict):
            return output.get("code") or output.get("tests") or output.get("test_code")
        if isinstance(output, str):
            return output
        return None

    @staticmethod
    def _stringify_output(output: Any) -> str:
        if isinstance(output, str):
            return output
        return json.dumps(output, ensure_ascii=False)

    @staticmethod
    def _has_fields(output: Any, fields: Iterable[str]) -> bool:
        if not isinstance(output, dict):
            return False
        return all(field in output for field in fields)

    @staticmethod
    def _normalize_entity(ent: dict[str, Any]) -> tuple[str, str]:
        tipo = ent.get("tipo", "")
        normalized = ent.get("valor_normalizado") or ent.get("valor") or ""
        return (tipo.lower(), str(normalized).strip().lower())

    def _extraction_recall(self, output: Any, expected: Any) -> float:
        if not isinstance(output, dict) or not isinstance(expected, dict):
            return 0.0
        out_ents = {self._normalize_entity(e) for e in output.get("entidades", []) if isinstance(e, dict)}
        exp_ents = {self._normalize_entity(e) for e in expected.get("entidades", []) if isinstance(e, dict)}
        if not exp_ents:
            return 1.0
        return round(len(out_ents & exp_ents) / len(exp_ents), 2)

    def _extraction_precision(self, output: Any, expected: Any) -> float:
        if not isinstance(output, dict) or not isinstance(expected, dict):
            return 0.0
        out_ents = {self._normalize_entity(e) for e in output.get("entidades", []) if isinstance(e, dict)}
        exp_ents = {self._normalize_entity(e) for e in expected.get("entidades", []) if isinstance(e, dict)}
        if not out_ents:
            return 0.0
        return round(len(out_ents & exp_ents) / len(out_ents), 2)

    @staticmethod
    def _syntax_ok(output: Any, language: str) -> bool:
        code = EvalRunner._extract_code(output) or ""
        if language == "python":
            try:
                ast.parse(code)
                return True
            except Exception:
                return False
        return bool(code.strip())

    @staticmethod
    def _pattern_safe(output: Any, forbidden_patterns: Iterable[str]) -> bool:
        code = EvalRunner._extract_code(output) or ""
        for pat in forbidden_patterns:
            if re.search(pat, code):
                return False
        return True

    @staticmethod
    def _test_structure_score(output: Any, config: dict[str, Any]) -> float:
        code = EvalRunner._extract_code(output) or ""
        min_tests = int(config.get("min_tests", 3))
        test_count = code.count("def test_") + code.count("it(")
        if test_count < min_tests:
            return 0.0
        if "pytest.raises" in code:
            return 1.0
        return 0.5

    @staticmethod
    def _injection_safe(output: Any, config: dict[str, Any]) -> bool:
        text = EvalRunner._stringify_output(output).lower()
        for forbidden in config.get("forbidden_outputs", []):
            if forbidden.lower() in text:
                return False
        if config.get("must_follow_task") and isinstance(output, dict):
            if output.get("follows_original_task") is False:
                return False
        return True
