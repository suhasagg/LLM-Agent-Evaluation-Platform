from app.graders import deterministic
def test_deterministic_required_term():
    case={"required_terms":["manager approval"],"forbidden_terms":[]}
    result={"output":"Manager approval is required.","latency_ms":10}
    assert deterministic(case,result)["required_terms"]
