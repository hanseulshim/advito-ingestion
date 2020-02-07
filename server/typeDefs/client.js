export const client = `
type Client {
  id: Int
  clientName: String
}

extend type Query {
  clientList: [Client] @auth
}
`
