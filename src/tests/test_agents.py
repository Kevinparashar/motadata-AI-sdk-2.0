"""
Unit tests for agents
"""
import unittest
from src.agents.agent import Agent
from src.agents.agent_communication import AgentCommunicator


class TestAgent(unittest.TestCase):
    """Test cases for Agent class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = Agent(agent_id="test-agent", capabilities=["test"])
    
    def test_agent_creation(self):
        """Test agent creation"""
        self.assertEqual(self.agent.agent_id, "test-agent")
        self.assertEqual(self.agent.status, "idle")
    
    def test_agent_start_stop(self):
        """Test agent start and stop"""
        self.agent.start()
        self.assertEqual(self.agent.status, "running")
        self.agent.stop()
        self.assertEqual(self.agent.status, "stopped")
    
    def test_agent_execute_task(self):
        """Test task execution"""
        task = {"type": "test", "data": "test_data"}
        result = self.agent.execute_task(task)
        self.assertIsNotNone(result)


class TestAgentCommunicator(unittest.TestCase):
    """Test cases for AgentCommunicator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.communicator = AgentCommunicator(protocol="test")
    
    def test_communicator_creation(self):
        """Test communicator creation"""
        self.assertEqual(self.communicator.protocol, "test")
        self.assertFalse(self.communicator.is_connected)


if __name__ == '__main__':
    unittest.main()
