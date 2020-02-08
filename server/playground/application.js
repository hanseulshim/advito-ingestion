export default {
  Query: {
    name: 'Application Queries',
    endpoint: '',
    headers: { sessiontoken: 'MY^PR3TTYP0NY' },
    query: `
     {
      applicationList {
        id
        applicationName
      }
    }`
  }
}
