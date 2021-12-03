import React, { useState } from "react";
import { Map, YMaps, ObjectManager } from "react-yandex-maps";
import { useQuery } from 'react-query';
import { fetchLitteredPoints } from '../../api';

const featuresExample = [
  {
    type: "Feature",
    id: 0,
    geometry: { type: "Point", coordinates: [55.831903, 37.411961] },
    properties: {
      balloonContentHeader:
        "<font size=3><b><a target='_blank' href='https://yandex.ru'>Здесь может быть ваша ссылка</a></b></font>",
      balloonContentBody:
        "<p>Ваше имя: <input name='login'></p><p><em>Телефон в формате 2xxx-xxx:</em>  <input></p><p><input type='submit' value='Отправить'></p>",
      balloonContentFooter:
        "<font size=1>Информация предоставлена: </font> <strong>этим балуном</strong>",
      clusterCaption: "<strong><s>Еще</s> одна</strong> метка",
      hintContent: "<strong>Текст  <s>подсказки</s></strong>",
    },
  },
]

const GarbageMap = () => {
  const { data } = useQuery('littered-points', fetchLitteredPoints)

  return (
    <YMaps>
      <Map
        defaultState={{ center: [55.75, 37.57], zoom: 9 }}
        width="100%"
        height="100%"
      >
        <ObjectManager
          options={{
            clusterize: true,
            gridSize: 32,
          }}
          objects={{
            openBalloonOnClick: true,
          }}
          clusters={{
          }}
          features={data?.map((point) => ({
            type: "Feature",
            id: point.cameraId,
            geometry: { type: "Point", coordinates: point.location },
            properties: {
              balloonContentHeader:
                "<font size=3><b><a target='_blank' href='https://yandex.ru'>Здесь может быть ваша ссылка</a></b></font>",
              balloonContentBody:
                "<p>Ваше имя: <input name='login'></p><p><em>Телефон в формате 2xxx-xxx:</em>  <input></p><p><input type='submit' value='Отправить'></p>",
              balloonContentFooter:
                "<font size=1>Информация предоставлена: </font> <strong>этим балуном</strong>",
              clusterCaption: "<strong><s>Еще</s> одна</strong> метка",
              hintContent: "<strong>Текст  <s>подсказки</s></strong>",
            },
          }))}
          modules={[
            "objectManager.addon.objectsBalloon",
            "objectManager.addon.objectsHint",
          ]}
        />
      </Map>
    </YMaps>
  );
};

export default GarbageMap;
