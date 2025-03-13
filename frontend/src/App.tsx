import useChat from './hooks/useChat'
import ChatWindow from './components/ChatWindow'

function App() {
  const {messages, sendMessage} = useChat()

  return (
    <>
      <div className ="min-h-screen bg-gray-100">
        <ChatWindow messages={messages} onSend={sendMessage}/>
      </div>
    </>
  )
}

export default App
