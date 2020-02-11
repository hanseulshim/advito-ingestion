import React from 'react'
import styled from 'styled-components'
import { Skeleton, Spin } from 'antd'

export const SkeletonLoader = () => <Skeleton active />

const SpinContainer = styled.div`
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
`
export const SpinLoader = () => (
  <SpinContainer>
    <Spin />
  </SpinContainer>
)
