import { ITask } from '@/shared/model/task.model';
import { IEmployee } from '@/shared/model/employee.model';

export interface IJob {
  id?: number;
  jobTitle?: string | null;
  minSalary?: number | null;
  maxSalary?: number | null;
  tasks?: ITask[] | null;
  employee?: IEmployee | null;
}

export class Job implements IJob {
  constructor(
    public id?: number,
    public jobTitle?: string | null,
    public minSalary?: number | null,
    public maxSalary?: number | null,
    public tasks?: ITask[] | null,
    public employee?: IEmployee | null
  ) {}
}
