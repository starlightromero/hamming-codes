const messages = document.getElementById('messages')
const sendButton = document.getElementById('sendButton')

let socket = io.connect('http://127.0.0.1:5000')

socket.on('connect', () => {
  socket.send('User has connected!')
})

socket.on('message', msg => {
  const li = document.createElement('li')
  li.appendChild(document.createTextNode(msg))
  messages.appendChild(li)
})

sendButton.addEventListener('click', () => {
  socket.send(newMessage.value)
  newMessage.value = ''
})
