export interface IFoo {
  id?: number;
  name?: string | null;
}

export class Foo implements IFoo {
  constructor(public id?: number, public name?: string | null) {}
}
