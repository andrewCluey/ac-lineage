import axios from 'axios';

const api = axios.create({
  });

if (import.meta.env.DEV) {
  api.defaults.baseURL = "http://localhost:8000/api/";
} else {
  api.defaults.baseURL = "/api/";
}
export const get_entities = async () => {
    const response = await api.get('entities/');
    return response.data;
}

export const get_entity = async (entity) => {
  const response = await api.get('entities/'+entity);
  return response.data;
}

export const get_entity_relations = async (entity) => {
      const response = await api.get('entities/relations/'+entity);
      return response.data;
  }

export const get_entity_relations_filtered = async (entity) => {
      const response = await api.get('entities/relations/'+entity+'/filtered');
      return response.data;
  }

export const refresh_cache = async () => {
    const response = await api.get('v1/refresh');
    return response.data;
}
