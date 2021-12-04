import { observer } from 'mobx-react-lite';
import React from 'react'
import styled from 'styled-components'
import GarbageMap from './GarbageMap';
import Stats from './Stats';

const Container = styled.section`
  width: 100%;
  height: 100%;
  padding: 1em;
  display: grid;
  grid-template-areas: "map stats";
  grid-template-rows: auto;
  grid-template-columns: 1fr 1fr;
  grid-gap: 1em;

  // @media(max-width: 900px) {
  //   grid-template-areas: "map";
  //   grid-template-rows: auto;
  //   grid-template-columns: auto;
  // }
`;

const Dashboard = () => {
  return (
    <Container>
      <GarbageMap />
      <Stats />
    </Container>
  )
}

export default observer(Dashboard);
