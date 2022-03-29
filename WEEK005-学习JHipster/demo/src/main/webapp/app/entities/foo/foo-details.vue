<template>
  <div class="row justify-content-center">
    <div class="col-8">
      <div v-if="foo">
        <h2 class="jh-entity-heading" data-cy="fooDetailsHeading"><span v-text="$t('demoApp.foo.detail.title')">Foo</span> {{ foo.id }}</h2>
        <dl class="row jh-entity-details">
          <dt>
            <span v-text="$t('demoApp.foo.name')">Name</span>
          </dt>
          <dd>
            <span>{{ foo.name }}</span>
          </dd>
        </dl>
        <button type="submit" v-on:click.prevent="previousState()" class="btn btn-info" data-cy="entityDetailsBackButton">
          <font-awesome-icon icon="arrow-left"></font-awesome-icon>&nbsp;<span v-text="$t('entity.action.back')"> Back</span>
        </button>
        <router-link v-if="foo.id" :to="{ name: 'FooEdit', params: { fooId: foo.id } }" custom v-slot="{ navigate }">
          <button @click="navigate" class="btn btn-primary">
            <font-awesome-icon icon="pencil-alt"></font-awesome-icon>&nbsp;<span v-text="$t('entity.action.edit')"> Edit</span>
          </button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts" src="./foo-details.component.ts"></script>
