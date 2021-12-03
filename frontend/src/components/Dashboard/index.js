import React from 'react'
import styled from 'styled-components'
import GarbageMap from './GarbageMap';

const Container = styled.section`
  width: 100%;
  height: 100%;
  padding: 1em;
  display: grid;
  grid-template-areas: "map";
  grid-template-rows: auto;
  grid-template-columns: auto;
  grid-gap: 1em;

  // @media(max-width: 900px) {
  //   grid-template-areas: "map";
  //   grid-template-rows: auto;
  //   grid-template-columns: auto;
  // }
`;

const Stats = styled.div`
  width: 100%;
  height: 100%;
`;

const Dashboard = () => {
  return (
    <Container>
      <GarbageMap />
    </Container>
  )
}

export default Dashboard;
