import React from "react";
import { Map, YMaps, ObjectManager } from "react-yandex-maps";
import { observer } from 'mobx-react-lite'
import useStore from "../../store"; 


const GarbageMap = () => {
  const store = useStore()

  return (
    <YMaps>
      <Map
        state={{
          center: [store.map.center_lat, store.map.center_alt],
          zoom: store.map.zoom
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
          features={store.cameras.map((camera) => ({
            type: "Feature",
            id: camera.id,
            geometry: { type: "Point", coordinates: camera.location },
            properties: {
              hintContent: `Заполненные баки: ${camera.filledContainers}`,
              balloonContentBody: camera?.photo && `<img src='${camera.photo}' width='300px'></img>`,
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

export default observer(GarbageMap);
