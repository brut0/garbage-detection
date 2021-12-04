import React from "react";
import { flow, types } from "mobx-state-tree";

export const GarbageContainer = types.model({
  insideGarbage: types.integer,
  nearbyGarbage: types.integer,
});

export const Camera = types
  .model({
    id: types.identifier,
    lat: types.number,
    alt: types.number,
    address: types.string,
    photo: types.maybeNull(types.string),
    filledContainers: types.integer,
    totalContainers: types.integer,
    containers: types.array(GarbageContainer),
  })
  .views((self) => ({
    get location() {
      return [self.lat, self.alt];
    },
    get nearbyGarbage() {
      return self.containers.reduce(
        (accumulate, item) => (accumulate + item.nearbyGarbage), 
        0
      );
    },
    get fullness() {
      if (self.totalContainers === 0) {
        return 0;
      }
      return (self.filledContainers / self.totalContainers) * 100;
    },
  }));

export const Map = types
  .model({
    center_lat: types.number,
    center_alt: types.number,
    zoom: types.number,
  })
  .views((self) => ({
    get center() {
      return [self.center_lat, self.center_alt];
    },
  }))
  .actions((self) => ({
    changeCenter([lat, alt]) {
      self.center_lat = lat;
      self.center_alt = alt;
    },
    changeZoom(zoom) {
      self.zoom = zoom;
    },
  }));

export const Store = types
  .model({
    cameras: types.array(Camera),
    map: Map,
    fetchingInterval: types.maybeNull(types.integer),
  })
  .actions((self) => ({
    fetchCameras: flow(function* () {
      let payload = [];
      try {
        const response = yield fetch("/api/cameras");
        payload = yield response.json();
        payload = payload.data
      } catch (error) {
        console.log(error);
        return;
      }

      self.cameras = payload.map(({ location, containers, ...item }) =>
        Camera.create({
          lat: location[0],
          alt: location[1],
          containers: containers.map((container) =>
            GarbageContainer.create({ ...container })
          ),
          ...item,
        })
      );
    }),
    afterCreate() {
      self.fetchCameras()
      self.fetchingInterval = setInterval(() => self.fetchCameras(), 15000);
    },
    beforeDestroy() {
      clearInterval(self.fetchingInterval);
    },
  }));

export const store = Store.create({
  cameras: [],
  map: Map.create({
    center_lat: 55.786778667350575,
    center_alt: 49.12538845509848,
    zoom: 12,
  }),
});

export const StoreContext = React.createContext(store);

export default function useStore() {
  return React.useContext(StoreContext);
}
