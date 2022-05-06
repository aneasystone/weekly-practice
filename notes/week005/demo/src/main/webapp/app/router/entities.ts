import { Authority } from '@/shared/security/authority';
/* tslint:disable */
// prettier-ignore
const Entities = () => import('@/entities/entities.vue');

// prettier-ignore
const Foo = () => import('@/entities/foo/foo.vue');
// prettier-ignore
const FooUpdate = () => import('@/entities/foo/foo-update.vue');
// prettier-ignore
const FooDetails = () => import('@/entities/foo/foo-details.vue');
// prettier-ignore
const Region = () => import('@/entities/region/region.vue');
// prettier-ignore
const RegionUpdate = () => import('@/entities/region/region-update.vue');
// prettier-ignore
const RegionDetails = () => import('@/entities/region/region-details.vue');
// prettier-ignore
const Country = () => import('@/entities/country/country.vue');
// prettier-ignore
const CountryUpdate = () => import('@/entities/country/country-update.vue');
// prettier-ignore
const CountryDetails = () => import('@/entities/country/country-details.vue');
// prettier-ignore
const Location = () => import('@/entities/location/location.vue');
// prettier-ignore
const LocationUpdate = () => import('@/entities/location/location-update.vue');
// prettier-ignore
const LocationDetails = () => import('@/entities/location/location-details.vue');
// prettier-ignore
const Department = () => import('@/entities/department/department.vue');
// prettier-ignore
const DepartmentUpdate = () => import('@/entities/department/department-update.vue');
// prettier-ignore
const DepartmentDetails = () => import('@/entities/department/department-details.vue');
// prettier-ignore
const Task = () => import('@/entities/task/task.vue');
// prettier-ignore
const TaskUpdate = () => import('@/entities/task/task-update.vue');
// prettier-ignore
const TaskDetails = () => import('@/entities/task/task-details.vue');
// prettier-ignore
const Employee = () => import('@/entities/employee/employee.vue');
// prettier-ignore
const EmployeeUpdate = () => import('@/entities/employee/employee-update.vue');
// prettier-ignore
const EmployeeDetails = () => import('@/entities/employee/employee-details.vue');
// prettier-ignore
const Job = () => import('@/entities/job/job.vue');
// prettier-ignore
const JobUpdate = () => import('@/entities/job/job-update.vue');
// prettier-ignore
const JobDetails = () => import('@/entities/job/job-details.vue');
// prettier-ignore
const JobHistory = () => import('@/entities/job-history/job-history.vue');
// prettier-ignore
const JobHistoryUpdate = () => import('@/entities/job-history/job-history-update.vue');
// prettier-ignore
const JobHistoryDetails = () => import('@/entities/job-history/job-history-details.vue');
// jhipster-needle-add-entity-to-router-import - JHipster will import entities to the router here

export default {
  path: '/',
  component: Entities,
  children: [
    {
      path: 'foo',
      name: 'Foo',
      component: Foo,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'foo/new',
      name: 'FooCreate',
      component: FooUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'foo/:fooId/edit',
      name: 'FooEdit',
      component: FooUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'foo/:fooId/view',
      name: 'FooView',
      component: FooDetails,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'region',
      name: 'Region',
      component: Region,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'region/new',
      name: 'RegionCreate',
      component: RegionUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'region/:regionId/edit',
      name: 'RegionEdit',
      component: RegionUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'region/:regionId/view',
      name: 'RegionView',
      component: RegionDetails,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'country',
      name: 'Country',
      component: Country,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'country/new',
      name: 'CountryCreate',
      component: CountryUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'country/:countryId/edit',
      name: 'CountryEdit',
      component: CountryUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'country/:countryId/view',
      name: 'CountryView',
      component: CountryDetails,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'location',
      name: 'Location',
      component: Location,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'location/new',
      name: 'LocationCreate',
      component: LocationUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'location/:locationId/edit',
      name: 'LocationEdit',
      component: LocationUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'location/:locationId/view',
      name: 'LocationView',
      component: LocationDetails,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'department',
      name: 'Department',
      component: Department,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'department/new',
      name: 'DepartmentCreate',
      component: DepartmentUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'department/:departmentId/edit',
      name: 'DepartmentEdit',
      component: DepartmentUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'department/:departmentId/view',
      name: 'DepartmentView',
      component: DepartmentDetails,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'task',
      name: 'Task',
      component: Task,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'task/new',
      name: 'TaskCreate',
      component: TaskUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'task/:taskId/edit',
      name: 'TaskEdit',
      component: TaskUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'task/:taskId/view',
      name: 'TaskView',
      component: TaskDetails,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'employee',
      name: 'Employee',
      component: Employee,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'employee/new',
      name: 'EmployeeCreate',
      component: EmployeeUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'employee/:employeeId/edit',
      name: 'EmployeeEdit',
      component: EmployeeUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'employee/:employeeId/view',
      name: 'EmployeeView',
      component: EmployeeDetails,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'job',
      name: 'Job',
      component: Job,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'job/new',
      name: 'JobCreate',
      component: JobUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'job/:jobId/edit',
      name: 'JobEdit',
      component: JobUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'job/:jobId/view',
      name: 'JobView',
      component: JobDetails,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'job-history',
      name: 'JobHistory',
      component: JobHistory,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'job-history/new',
      name: 'JobHistoryCreate',
      component: JobHistoryUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'job-history/:jobHistoryId/edit',
      name: 'JobHistoryEdit',
      component: JobHistoryUpdate,
      meta: { authorities: [Authority.USER] },
    },
    {
      path: 'job-history/:jobHistoryId/view',
      name: 'JobHistoryView',
      component: JobHistoryDetails,
      meta: { authorities: [Authority.USER] },
    },
    // jhipster-needle-add-entity-to-router - JHipster will add entities to the router here
  ],
};
