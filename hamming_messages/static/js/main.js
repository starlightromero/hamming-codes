/*  global
    axios
*/

window.addEventListener('DOMContentLoaded', () => {
  const messages = document.getElementById('messages')
  const sendButton = document.getElementById('sendButton')
  const newMessage = document.getElementById('newMessage')
  let onlineUsersList = document.getElementById('onlineUsers')
  let offlineUsersList = document.getElementById('offlineUsers')
  let onlineUsers = onlineUsersList.querySelectorAll('li')
  let offlineUsers = offlineUsersList.querySelectorAll('li')

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

  const removeMessages = list => {
    while (list.firstChild) {
      list.removeChild(list.firstChild)
    }
  }

  const updateMessages = messages => {
    const sender = document.getElementById('sender').innerHTML
    const messageList = document.getElementById('messages')

    removeMessages(messageList)

    for (message in messages) {
      messageSender = document.createElement('li')
      messageText = document.createElement('li')
      messageSender.appendChild(document.createTextNode(messages[message]['sender']))
      messageText.appendChild(document.createTextNode(messages[message]['message']))
      messageSender.classList.add('sender')
      messageText.classList.add('message')
      ul = document.createElement('ul')
      ul.appendChild(messageSender)
      ul.appendChild(messageText)

      if (messages[message]['sender'] === sender) {
        ul.classList.add('sentMessage')
      } else {
        ul.classList.add('receivedMessage')
      }

      messageList.appendChild(ul)
    }
  }

  const getMessages = room => {
    async function getMessagesRequest () {
      try {
        let response = await axios({
          method: 'GET',
          url: '/messages/' + room.innerHTML
        })
        if (response) {
          updateMessages(response.data)
        }
      } catch (error) {
        console.log(error)
      }
    }
    getMessagesRequest()
  }

  const leaveRoom = room => {
    const sender = document.getElementById('sender').innerHTML
    socket.emit('leave', {'username': sender, 'room': room.innerHTML})
  }

  const joinRoom = room => {
    const sender = document.getElementById('sender').innerHTML
    socket.emit('join', {'username': sender, 'room': room.innerHTML})
    document.getElementById('currentRoom').innerHTML = room.innerHTML
    getMessages(room)
    scrollBottom()
  }

  const openBackdrop = () => {
    document.querySelector('.backdrop').style.display = 'block'
  }

  const closeBackdrop = () => {
    document.querySelector('.backdrop').style.display = 'none'
  }

  const clearAddRoomModal = () => {
    document.querySelector('.roomName').value = ''
    document.querySelector('.roomDescription').value = ''
  }

  const openAddRoomModal = () => {
    openBackdrop()
    document.querySelector('.addRoomModal').style.display = 'block'
  }

  const closeAddRoomModal = () => {
    clearAddRoomModal()
    document.querySelector('.addRoomModal').style.display = 'none'
    closeBackdrop()
  }

  const openSettingsModal = () => {
    openBackdrop()
    document.querySelector('.settingsModal').style.display = 'block'
  }

  const closeSettingsModal = () => {
    document.querySelector('.settingsModal').style.display = 'none'
    closeBackdrop()
  }

  const updatePastMessages = (oldSender, newSender) => {
    const sentMessages = document.querySelectorAll('.sentMessage')
    for (const message of sentMessages) {
      message.querySelector('.sender').innerHTML = newSender
    }
  }

  const updateSender = sender => {
    const oldUsername = document.getElementById('sender')
    updatePastMessages(oldUsername, sender)
    onlineUsers = onlineUsersList.querySelectorAll('li')
    for (user of onlineUsers) {
      if (user.innerHTML === oldUsername.innerHTML) {
        user.innerHTML = sender
      }
    }
    oldUsername.innerHTML = sender
  }

  const getUser = () => {
    async function getUserRequest () {
      try {
        let response = await axios({
          method: 'GET',
          url: '/user'
        })
        if (response) {
          updateSender(response.data.username)
          joinRoom(document.getElementById('currentRoom'))
        }
      } catch (error) {
        console.log(error)
      }
    }
    getUserRequest()
  }

  // SOCKETS

  let socket = io.connect('http://127.0.0.1:5000')

  joinRoom(document.getElementById('currentRoom'))

  socket.on('connect', () => {
    scrollBottom()
    const sender = document.getElementById('sender').innerHTML
    socket.emit('userOnline', {'username': sender})
  })

  socket.on('userOnline', username => {
    userOnline(username)
  })

  socket.on('userOffline', username => {
    userOffline(username)
  })

  socket.on('message', data => {
    const sender = document.getElementById('sender').innerHTML
    if (data['message'] && data['sender']) {
      const ul = document.createElement('ul')
      data['sender'] === sender ? ul.classList.add('sentMessage') : ul.classList.add('receivedMessage')
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

  // CHANGE ROOM

  const changeRoom = room => {
    room.onclick = () => {
      leaveRoom(document.getElementById('currentRoom'))
      joinRoom(room)
    }
  }

  document.querySelectorAll('.room').forEach(room => {
    changeRoom(room)
  })

  // DELETE ROOM

  const removeRoomFromList = roomToRemove => {
    document.querySelectorAll('.room').forEach(room => {
      if (room.innerHTML === roomToRemove) {
        room.remove()
      }
    })
  }

  const longPressRoomToDelete = room => {
    room.addEventListener('long-press', event => {
      event.target.classList.add('shake')
      async function deleteRoom () {
        try {
          let response = await axios({
            method: 'DELETE',
            url: '/room',
            data: {
              'name': event.target.innerHTML
            }
          })
          if (response) {
            removeRoomFromList(response.data)
          }
        } catch (error) {
          console.log(error)
        }
      }
      deleteRoom()
    })
  }

  document.querySelectorAll('.room').forEach(room => {
    longPressRoomToDelete(room)
  })

  // MESSAGES

  newMessage.addEventListener('keypress', event => {
    // console.log(event.keyCode)
    //
    //
    //
    if (event.keyCode === 13) {
      event.preventDefault()
      sendButton.click()
    }
  })

  sendButton.addEventListener('click', () => {
    const sender = document.getElementById('sender').innerHTML
    if (newMessage.value) {
      socket.send({'message': newMessage.value, 'sender': sender})
    }
    newMessage.value = ''
  })

  document.getElementById('disruptedSendButton').addEventListener('click', () => {
    const sender = document.getElementById('sender').innerHTML
    socket.send({'message': newMessage.value, 'sender': sender})
    newMessage.value = ''
  })

  // USERS LISTS

  document.getElementById('onlineUsers').addEventListener('click', event => {
    console.log(event.target.innerHTML)
  })

  document.getElementById('offlineUsers').addEventListener('click', event => {
    console.log(event.target.innerHTML)
  })

  // BACKDROP

  document.querySelector('.backdrop').addEventListener('click', () => {
    closeAddRoomModal()
    closeSettingsModal()
  })

  // ADD ROOM

  document.getElementById('addRoomButton').addEventListener('click', () => {
    openAddRoomModal()
  })

  document.querySelector('.closeAddRoom').addEventListener('click', () => {
    closeAddRoomModal()
  })

  document.querySelector('.addRoomFormSubmit').addEventListener('click', event => {
    event.preventDefault()
    async function sendRoomRequest () {
      try {
        let response = await axios({
          method: 'PUT',
          url: '/room',
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
          changeRoom(li)
          longPressRoomToDelete(li)
          leaveRoom(document.getElementById('currentRoom'))
          joinRoom(li)
        }
      } catch (error) {
        console.log(error)
        clearAddRoomModal()
      }
    }
    sendRoomRequest()
  })

  // SETTINGS

  document.getElementById('settingsButton').addEventListener('click', () => {
    openSettingsModal()
  })

  document.querySelector('.closeSettings').addEventListener('click', () => {
    closeSettingsModal()
  })

  document.getElementById('signout').addEventListener('click', () => {
    const sender = document.getElementById('sender').innerHTML
    socket.emit('userOffline', {'username': sender})
    window.location.href = '/signout'
  })

  document.querySelector('.updatedSubmit').addEventListener('click', () => {
    event.preventDefault()
    async function sendUpdateAccount () {
      try {
        let response = await axios({
          method: 'PATCH',
          url: '/update',
          data: {
            'username': document.querySelector('.updatedUsername').value,
            'email': document.querySelector('.updatedEmail').value
          }
        })
        if (response) {
          closeSettingsModal()
          getUser()
        }
      } catch (error) {
        console.log(error)
      }
    }
    sendUpdateAccount()
  })
})
