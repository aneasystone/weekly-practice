import { IRegion } from '@/shared/model/region.model';

export interface ICountry {
  id?: number;
  countryName?: string | null;
  region?: IRegion | null;
}

export class Country implements ICountry {
  constructor(public id?: number, public countryName?: string | null, public region?: IRegion | null) {}
}
