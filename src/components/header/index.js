import React from 'react'
import { useLocation } from 'react-router'
import TopHeader from './TopHeader'
import BreadCrumbs from './BreadCrumbs'

const Header = () => {
  const location = useLocation()
  return (
    <>
      <TopHeader />
      {location.pathname !== '/' && <BreadCrumbs />}
    </>
  )
}

export default Header
