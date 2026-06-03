export interface User {
  id: number;
  email: string;
  name: string;
  tenant_id: number;
  store_id: number | null;
  roles: string[];
}