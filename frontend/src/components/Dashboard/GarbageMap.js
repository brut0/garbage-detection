import React from "react";
import { Map, YMaps, ObjectManager } from "react-yandex-maps";
import { useQuery } from "react-query";
import { fetchLitteredPoints } from "../../api";

const GarbageMap = () => {
  const { data } = useQuery("littered-points", fetchLitteredPoints, {
    refetchInterval: 15000
  });

  return (
    <YMaps>
      <Map
        defaultState={{
          center: [55.786778667350575, 49.12538845509848],
          zoom: 12,
        }}
        width="100%"
        height="100%"
        modules={["templateLayoutFactory", "layout.ImageWithContent"]}
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
          features={data?.map((camera) => ({
            type: "Feature",
            id: camera.id,
            geometry: { type: "Point", coordinates: camera.location },
            properties: {
              hintContent: `Заполненные баки: ${camera.filledContainers}`,
              balloonContentBody: camera?.photo && `<img src='${camera.photo}' width='400px'></img>`,
            },
            options: {
              preset: 'islands#circleDotIcon',
              iconColor: camera.filledContainers > 0 ? 'red' : 'green'
            }
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
