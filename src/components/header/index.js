import React from 'react'
import { useLocation } from 'react-router'
import TopHeader from './TopHeader'

const Header = () => {
  const location = useLocation()
  return (
    <>
      <TopHeader />
    </>
  )
}

export default Header
