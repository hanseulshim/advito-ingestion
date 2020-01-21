const { override, fixBabelImports, addLessLoader } = require('customize-cra')

module.exports = override(
  fixBabelImports('import', {
    libraryName: 'antd',
    libraryDirectory: 'es',
    style: true
  }),
  addLessLoader({
    javascriptEnabled: true,
    modifyVars: {
      '@primary-color': '#4baaa3',
      '@btn-default-color': '#FFF',
      '@btn-default-bg': '#4baaa3',
      '@btn-default-border': '#4baaa3',
      '@btn-danger-color': '#FFF',
      '@btn-danger-bg': '#FF9E16',
      '@btn-danger-border': '#FF9E16'
    }
  })
)
