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

      templateList(applicationId: null) {
        id
        templateName
        applicationName
        templatePath
      }

      sampleTemplateList{
        id
        templateName
        applicationName
        templatePath
      }

      sourceList(templateId: null) {
        id
        sourceName
      }
    }`
  }
}
