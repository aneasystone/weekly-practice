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
    // jhipster-needle-add-entity-to-router - JHipster will add entities to the router here
  ],
};
