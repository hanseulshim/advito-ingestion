export default {
  Query: {
    name: 'Client Queries',
    endpoint: '',
    headers: { sessiontoken: 'MY^PR3TTYP0NY' },
    query: `
     {
      clientList {
        id
        clientName
      }
    }`
  }
}
