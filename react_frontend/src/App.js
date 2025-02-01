import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Row, Col, Card, Button, Form, ListGroup } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [agents, setAgents] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [files, setFiles] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  // Fetch initial data
  useEffect(() => {
    fetchAgents();
    fetchTasks();
    fetchFiles();
  }, []);

  // API calls
  const fetchAgents = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/agents');
      setAgents(response.data.agents);
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  const fetchTasks = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/tasks');
      setTasks(response.data.tasks);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  const fetchFiles = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/filesystem');
      setFiles(response.data.files);
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  const sendMessage = async () => {
    if (!selectedAgent || !message.trim()) return;

    try {
      const response = await axios.post('http://localhost:5000/api/chat', {
        message,
        agent_id: selectedAgent
      });

      setChatHistory([...chatHistory, 
        { type: 'user', content: message },
        { type: 'agent', content: response.data.message }
      ]);
      setMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <Container fluid className="p-4">
      <Row>
        {/* Sidebar */}
        <Col md={3}>
          <Card className="mb-4">
            <Card.Header>Agents</Card.Header>
            <ListGroup variant="flush">
              {agents.map(agent => (
                <ListGroup.Item 
                  key={agent.id}
                  action
                  active={selectedAgent === agent.id}
                  onClick={() => setSelectedAgent(agent.id)}
                >
                  {agent.name}
                </ListGroup.Item>
              ))}
            </ListGroup>
          </Card>

          <Card className="mb-4">
            <Card.Header>Tasks</Card.Header>
            <ListGroup variant="flush">
              {tasks.map(task => (
                <ListGroup.Item key={task.id}>
                  {task.name} - {task.status}
                </ListGroup.Item>
              ))}
            </ListGroup>
          </Card>

          <Card>
            <Card.Header>Files</Card.Header>
            <ListGroup variant="flush">
              {files.map((file, index) => (
                <ListGroup.Item key={index}>
                  {file.name} ({file.type})
                </ListGroup.Item>
              ))}
            </ListGroup>
          </Card>
        </Col>

        {/* Main Chat Area */}
        <Col md={9}>
          <Card className="chat-container">
            <Card.Header>
              Chat {selectedAgent ? `with Agent ${selectedAgent}` : ''}
            </Card.Header>
            <Card.Body style={{ height: '600px', overflowY: 'auto' }}>
              {chatHistory.map((msg, index) => (
                <div key={index} className={`message ${msg.type}`}>
                  <strong>{msg.type === 'user' ? 'You' : 'Agent'}:</strong>
                  <p>{msg.content}</p>
                </div>
              ))}
            </Card.Body>
            <Card.Footer>
              <Form onSubmit={e => { e.preventDefault(); sendMessage(); }}>
                <Row>
                  <Col>
                    <Form.Control
                      type="text"
                      value={message}
                      onChange={e => setMessage(e.target.value)}
                      placeholder="Type your message..."
                      disabled={!selectedAgent}
                    />
                  </Col>
                  <Col xs="auto">
                    <Button 
                      type="submit"
                      disabled={!selectedAgent || !message.trim()}
                    >
                      Send
                    </Button>
                  </Col>
                </Row>
              </Form>
            </Card.Footer>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default App;