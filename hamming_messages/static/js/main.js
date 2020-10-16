const messages = document.getElementById('messages')
const sendButton = document.getElementById('sendButton')
const newMessage = document.getElementById('newMessage')
const sender = document.getElementById('sender').innerHTML
const onlineUsersList = document.getElementById('onlineUsers')
const offlineUsersList = document.getElementById('offlineUsers')
const onlineUsers = onlineUsersList.querySelectorAll('li')
const offlineUsers = offlineUsersList.querySelectorAll('li')
const addRoomButton = document.getElementById('addRoomButton')
const rooms = document.querySelectorAll('.room')

const scrollBottom = () => {
  messages.scrollTop = messages.scrollHeight
}

const leaveRoom = room => {
  socket.emit('leave', {'username': sender, 'room': room})
}

const joinRoom = room => {
  socket.emit('join', {'username': sender, 'room': room})
}

let socket = io.connect('http://127.0.0.1:5000')

let room = 'lounge'
joinRoom('lounge')

socket.on('connect', () => {
  socket.emit('usernameConnected', sender)
  scrollBottom()
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
  } else if (data['message']) {
    const p = document.createElement('p')
    p.appendChild(document.createTextNode(data['message']))
    messages.appendChild(p)
  } else {
    const p = document.createElement('p')
    p.appendChild(document.createTextNode(data))
    messages.appendChild(p)
  }
  scrollBottom()
})

socket.on('disconnect', () => {
  console.log(sender)
  socket.emit('usernameDisconnected', sender)
})

rooms.forEach(room => {
  room.onclick = () => {
    let newRoom = room.innerHTML
    if (newRoom === room) {
      message = `You are already in ${room} room.`
      // printSysMsg(msg)
    } else {
      leaveRoom(room)
      joinRoom(newRoom)
      room = newRoom
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

onlineUsersList.addEventListener('click', event => {
  const username = event.target.innerHTML
  alert(`DM ${username}`)
})

offlineUsersList.addEventListener('click', event => {
  const username = event.target.innerHTML
  alert(`DM ${username}`)
})

addRoomButton.addEventListener('click', () => {
  alert('Added Chat Room')
})
