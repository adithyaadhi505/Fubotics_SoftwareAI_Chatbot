import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './App.css'
import ParticleBackground from './components/ParticleBackground'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function App() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [userEmail, setUserEmail] = useState(localStorage.getItem('userEmail') || '')
  const [showEmailInput, setShowEmailInput] = useState(!localStorage.getItem('userEmail'))
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    const messageDate = new Date(date.getFullYear(), date.getMonth(), date.getDate())
    const todayDate = new Date(today.getFullYear(), today.getMonth(), today.getDate())
    const yesterdayDate = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate())

    if (messageDate.getTime() === todayDate.getTime()) {
      return 'Today'
    } else if (messageDate.getTime() === yesterdayDate.getTime()) {
      return 'Yesterday'
    } else {
      return date.toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit', year: 'numeric' })
    }
  }

  const shouldShowDateSeparator = (currentMessage, previousMessage) => {
    if (!previousMessage) return true
    
    const currentDate = new Date(currentMessage.created_at).toDateString()
    const previousDate = new Date(previousMessage.created_at).toDateString()
    
    return currentDate !== previousDate
  }

  useEffect(() => {
    if (userEmail) {
      fetchMessages()
    }
  }, [userEmail])

  const fetchMessages = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/messages`, {
        params: { email: userEmail }
      })
      setMessages(response.data)
      setError(null)
    } catch (err) {
      console.error('Error fetching messages:', err)
      setError('Failed to load chat history')
    }
  }

  const handleEmailSubmit = (e) => {
    e.preventDefault()
    const email = userEmail.trim().toLowerCase()
    if (email && email.includes('@')) {
      localStorage.setItem('userEmail', email)
      setUserEmail(email)
      setShowEmailInput(false)
      setError(null)
    } else {
      setError('Please enter a valid email address')
    }
  }

  const handleChangeEmail = () => {
    setShowEmailInput(true)
    setMessages([])
  }

  const sendMessage = async (e) => {
    e.preventDefault()
    
    if (!inputValue.trim()) return

    const userMessage = inputValue.trim()
    setInputValue('')
    setIsLoading(true)
    setError(null)

    const tempUserMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString()
    }
    setMessages(prev => [...prev, tempUserMessage])

    try {
      const response = await axios.post(`${API_BASE_URL}/api/messages`, {
        content: userMessage,
        email: userEmail
      })

      setMessages(prev => {
        const filtered = prev.filter(msg => msg.id !== tempUserMessage.id)
        return [...filtered, response.data.user_message, response.data.ai_message]
      })
    } catch (err) {
      console.error('Error sending message:', err)
      setError('Failed to send message. Please try again.')
      setMessages(prev => prev.filter(msg => msg.id !== tempUserMessage.id))
    } finally {
      setIsLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage(e)
    }
  }

  return (
    <div className="app">
      <ParticleBackground />
      {showEmailInput ? (
        <div className="email-modal">
          <div className="email-card">
            <div className="email-header">
              <div className="email-icon">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" fill="currentColor"/>
                </svg>
              </div>
              <h2>Welcome to AI Chat</h2>
              <p>Enter your email to start chatting</p>
            </div>
            <form onSubmit={handleEmailSubmit} className="email-form">
              <input
                type="email"
                value={userEmail}
                onChange={(e) => setUserEmail(e.target.value)}
                placeholder="your.email@example.com"
                className="email-input"
                required
                autoFocus
              />
              <button type="submit" className="email-submit-btn">
                Start Chatting
              </button>
            </form>
            {error && (
              <div className="email-error">
                {error}
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="chat-container">
          <header className="chat-header">
            <div className="header-content">
              <div className="bot-avatar">
                <div className="avatar-icon">
                  <img src="/assets/ai_img.png" alt="AI Assistant" />
                </div>
              </div>
              <div className="header-text">
                <h1>AI Assistant</h1>
                <p className="status-text">{userEmail}</p>
              </div>
              <button onClick={handleChangeEmail} className="new-chat-btn">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" fill="currentColor"/>
                </svg>
                New Chat
              </button>
            </div>
          </header>

        <div className="messages-container">
          {messages.length === 0 && !error && (
            <div className="empty-state">
              <div className="empty-icon">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z" fill="currentColor"/>
                </svg>
              </div>
              <h2>Start a conversation</h2>
              <p>Send a message to begin chatting with the AI assistant</p>
            </div>
          )}

          {error && (
            <div className="error-message">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" fill="currentColor"/>
              </svg>
              {error}
            </div>
          )}

          {messages.map((message, index) => (
            <React.Fragment key={message.id}>
              {shouldShowDateSeparator(message, messages[index - 1]) && (
                <div className="date-separator">
                  <span className="date-separator-line"></span>
                  <span className="date-separator-text">
                    {formatDate(message.created_at)}
                  </span>
                  <span className="date-separator-line"></span>
                </div>
              )}
              <div
                className={`message ${message.role === 'user' ? 'user-message' : 'ai-message'}`}
              >
                <div className="message-avatar">
                  {message.role === 'assistant' ? (
                    <div className="ai-avatar">
                      <img src="/assets/ai_img.png" alt="AI" />
                    </div>
                  ) : (
                    <div className="user-avatar">
                      <img src="/assets/human_img.png" alt="User" />
                    </div>
                  )}
                </div>
                <div className="message-content">
                  <div className="message-bubble">
                    {message.content}
                  </div>
                  <div className="message-time">
                    {new Date(message.created_at).toLocaleTimeString([], { 
                      hour: '2-digit', 
                      minute: '2-digit' 
                    })}
                  </div>
                </div>
              </div>
            </React.Fragment>
          ))}

          {isLoading && (
            <div className="message ai-message">
              <div className="message-avatar">
                <div className="ai-avatar">
                  <img src="/assets/ai_img.png" alt="AI" />
                </div>
              </div>
              <div className="message-content">
                <div className="message-bubble typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <footer className="chat-footer">
          <form onSubmit={sendMessage} className="input-form">
            <div className="input-wrapper">
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                disabled={isLoading}
                className="message-input"
              />
              <button
                type="submit"
                disabled={isLoading || !inputValue.trim()}
                className="send-button"
                title="Send message"
              >
                <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M10 8 L10 24 L24 16 Z M10 8 L24 16 M10 24 L24 16" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="miter" fill="none"/>
                </svg>
              </button>
            </div>
          </form>
        </footer>
        </div>
      )}
    </div>
  )
}

export default App
