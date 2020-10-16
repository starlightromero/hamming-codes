const messages = document.getElementById('messages')
const sendButton = document.getElementById('sendButton')
const newMessage = document.getElementById('newMessage')
const sender = document.getElementById('sender').innerHTML
const onlineUsersList = document.getElementById('onlineUsers')

let socket = io.connect('http://127.0.0.1:5000')

socket.on('connect', () => {
  socket.emit('usernameConnected', sender)
})

socket.on('message', data => {
  if (data['message'] && data['sender']) {
    const ul = document.createElement('ul')
    const sender = document.createElement('li')
    const message = document.createElement('li')
    sender.appendChild(document.createTextNode(data['sender']))
    message.appendChild(document.createTextNode(data['message']))
    ul.appendChild(sender)
    ul.appendChild(message)
    messages.appendChild(ul)
  } else {
    const p = document.createElement('p')
    p.appendChild(document.createTextNode(data))
    messages.appendChild(p)
  }
})

socket.on('usernameConnected', data => {
  console.log(data)
  // const p = document.createElement('p')
  // p.appendChild(document.createTextNode(data))
  // messages.appendChild(p)
  // const onlineUsers = onlineUsersList.querySelectorAll('li')
  // for (user of onlineUsers) {
  //   console.log(user.innerHTML)
  //   if (user.innerHTML === username) {
  //     console.log('yes')
  //   }
  // }
})

socket.on('disconnect', () => {
  console.log(sender)
  socket.emit('usernameDisconnected', sender)
})

socket.on('usernameDisconnected', data => {
  console.log(data)
  const p = document.createElement('p')
  p.appendChild(document.createTextNode(data))
  messages.appendChild(p)
  const onlineUsers = onlineUsersList.querySelectorAll('li')
  for (user of onlineUsers) {
    console.log(user.innerHTML)
    if (user.innerHTML === username) {
      console.log('yes')
    }
  }
})

newMessage.addEventListener('keyup', event => {
  if (event.keyCode === 13) {
    event.preventDefault()
    sendButton.click()
  }
})

sendButton.addEventListener('click', () => {
  socket.send({'message': newMessage.value, 'sender': sender})
  newMessage.value = ''
})
