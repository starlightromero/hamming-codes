const messages = document.getElementById('messages')
const sendButton = document.getElementById('sendButton')
const newMessage = document.getElementById('newMessage')
const sender = document.getElementById('sender').innerHTML
const onlineUsersList = document.getElementById('onlineUsers')
const offlineUsersList = document.getElementById('offlineUsers')
const onlineUsers = onlineUsersList.querySelectorAll('li')
const offlineUsers = offlineUsersList.querySelectorAll('li')

const scrollBottom = () => {
  messages.scrollTop = messages.scrollHeight
}

let socket = io.connect('http://127.0.0.1:5000')

socket.on('connect', () => {
  socket.emit('usernameConnected', sender)
})

socket.on('message', data => {
  if (data['message'] && data['sender']) {
    const ul = document.createElement('ul')
    data['sender'] === sender ? ul.classList.add('sent-message') : ul.classList.add('received-message')
    const senderli = document.createElement('li')
    const messageli = document.createElement('li')
    senderli.appendChild(document.createTextNode(data['sender']))
    messageli.appendChild(document.createTextNode(data['message']))
    senderli.classList.add('sender')
    messageli.classList.add('message')
    ul.appendChild(senderli)
    ul.appendChild(messageli)
    messages.appendChild(ul)
  } else {
    const p = document.createElement('p')
    p.appendChild(document.createTextNode(data))
    messages.appendChild(p)
  }
  scrollBottom()
})

socket.on('usernameConnected', data => {
  console.log(data)
  scrollBottom()
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

onlineUsersList.addEventListener('click', event => {
  const username = event.target.innerHTML
  alert(`DM ${username}`)
})

offlineUsersList.addEventListener('click', event => {
  const username = event.target.innerHTML
  alert(`DM ${username}`)
})
