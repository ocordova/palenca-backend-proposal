import { createServer } from 'http'
import { Server } from 'socket.io'
import { config } from './config'

const httpServer = createServer()

export const io = new Server(httpServer, {
  cors: {
    origin: '*'
  }
})

io.on('connection', () => {
  console.log('a user connected')

  io.on('disconnect', () => {
    console.log('user disconnected')
  })
})

httpServer.listen(config.port, () => {
  console.log(
    `Socket.io is running at http://localhost:${config.port}`
  )
})
