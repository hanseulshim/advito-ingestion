import { createGlobalStyle } from 'styled-components'

export default createGlobalStyle`
  html,
  body, #root {
    height:100%
  }
  #root {
    margin: 0;
    padding: 0;
    font-family: 'Rubik', sans-serif;
    background: ${props => props.theme.white};
    color: ${props => props.theme.doveGray};
    font-weight: 300;
    font-size: 16px;
    line-height: 20px;
    
    @media (max-width : 1336px){
      font-size: 14px;
      line-height: 17px;
    }
  }
  a {
    text-decoration: none;
  }

`
