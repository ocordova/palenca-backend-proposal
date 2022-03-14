export interface Config {
  port: number
}

export const config: Config = {
  port: Number(process.env.PORT) || 3000
}
