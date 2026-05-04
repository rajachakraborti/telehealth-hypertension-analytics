import pytest
from app.services.pipeline.workflow_engine import WorkflowEngine

@pytest.fixture
def workflow_engine():
    return WorkflowEngine()

def test_initialize_workflow(workflow_engine):
    assert workflow_engine is not None
    assert workflow_engine.current_step == 0

def test_add_step(workflow_engine):
    workflow_engine.add_step("Data Ingestion")
    assert len(workflow_engine.steps) == 1
    assert workflow_engine.steps[0] == "Data Ingestion"

def test_execute_step(workflow_engine):
    workflow_engine.add_step("Data Ingestion")
    result = workflow_engine.execute_step(0)
    assert result == "Data Ingestion executed"

def test_execute_invalid_step(workflow_engine):
    with pytest.raises(IndexError):
        workflow_engine.execute_step(10)

def test_workflow_progress(workflow_engine):
    workflow_engine.add_step("Data Ingestion")
    workflow_engine.add_step("Data Cleaning")
    workflow_engine.execute_step(0)
    assert workflow_engine.current_step == 1
    workflow_engine.execute_step(1)
    assert workflow_engine.current_step == 2

def test_reset_workflow(workflow_engine):
    workflow_engine.add_step("Data Ingestion")
    workflow_engine.execute_step(0)
    workflow_engine.reset()
    assert workflow_engine.current_step == 0
    assert len(workflow_engine.steps) == 1