from app.datasets import load
def test_dataset():
    d=load("support-v1")
    assert d["version"]=="1.0.0" and len(d["cases"])>=2
