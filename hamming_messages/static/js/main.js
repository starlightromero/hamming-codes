/*  global
    axios
*/

window.addEventListener('DOMContentLoaded', () => {
  const messages = document.getElementById('messages')
  const sendButton = document.getElementById('sendButton')
  const newMessage = document.getElementById('newMessage')
  const sender = document.getElementById('sender').innerHTML
  let onlineUsersList = document.getElementById('onlineUsers')
  let offlineUsersList = document.getElementById('offlineUsers')
  let onlineUsers = onlineUsersList.querySelectorAll('li')
  let offlineUsers = offlineUsersList.querySelectorAll('li')
  let roomList = document.querySelectorAll('.room')

  // HELPER FUNCTIONS

  const scrollBottom = () => {
    messages.scrollTop = messages.scrollHeight
  }

  const userOnline = username => {
    for (user of offlineUsers) {
      if (user.innerHTML === username) {
        user.remove()
        onlineUsersList.appendChild(user)
      }
    }
  }

  const userOffline = username => {
    onlineUsersList = document.getElementById('onlineUsers')
    offlineUsersList = document.getElementById('offlineUsers')
    onlineUsers = onlineUsersList.querySelectorAll('li')
    for (user of onlineUsers) {
      if (user.innerHTML === username) {
        user.remove()
        offlineUsersList.appendChild(user)
      }
    }
  }

  const leaveRoom = room => {
    socket.emit('leave', {'username': sender, 'room': room})
  }

  const joinRoom = room => {
    socket.emit('join', {'username': sender, 'room': room})
  }

  const clearAddRoomModal = () => {
    document.querySelector('.roomName').value = ''
    document.querySelector('.roomDescription').value = ''
  }

  const closeAddRoomModal = () => {
    clearAddRoomModal()
    document.querySelector('.addRoomModal').style.display = 'none'
    document.querySelector('.backdrop').style.display = 'none'
  }

  // SOCKETS

  let socket = io.connect('http://127.0.0.1:5000')

  let room = 'lounge'
  joinRoom('lounge')

  socket.on('connect', () => {
    scrollBottom()
    socket.emit('userOnline', {'username': sender})
  })

  socket.on('userOnline', username => {
    userOnline(username)
  })

  socket.on('userOffline', username => {
    userOffline(username)
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

  roomList.forEach(room => {
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

  // EVENT LISTENERS

  document.getElementById('settingsButton').addEventListener('click', () => {
    socket.emit('userOffline', {'username': sender})
    window.location.href = '/signout'
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

  document.getElementById('addRoomButton').addEventListener('click', () => {
    document.querySelector('.addRoomModal').style.display = 'block'
    document.querySelector('.backdrop').style.display = 'block'
  })

  document.querySelector('.backdrop').addEventListener('click', () => {
    closeAddRoomModal()
  })

  document.querySelector('.close').addEventListener('click', () => {
    closeAddRoomModal()
  })

  document.querySelector('.addRoomFormSubmit').addEventListener('click', event => {
    event.preventDefault()
    async function sendRoomRequest () {
      try {
        let response = await axios({
          method: 'PUT',
          url: '/add-room',
          data: {
            'name': document.querySelector('.roomName').value,
            'description': document.querySelector('.roomDescription').value
          }
        })
        if (response) {
          closeAddRoomModal()
          const rooms = document.querySelector('.rooms')
          const li = document.createElement('li')
          li.appendChild(document.createTextNode(response.data))
          li.classList.add('room')
          rooms.appendChild(li)
        }
      } catch (error) {
        console.log(error)
        clearAddRoomModal()
      }
    }
    async function updateRoomList () {
      await sendRoomRequest()
      roomList = document.querySelectorAll('.room')
    }
    updateRoomList()
  })
})
