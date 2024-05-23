<script>
import KnownFaces from '../components/KnownFaces.vue'
import AddingUnknownForm from '../components/AddingUnknownForm.vue'
import Log from '../components/Log.vue'

export default {
  components: {
    KnownFaces,
    AddingUnknownForm,
    Log
  }
}
</script>

<template>
    <div class="Admin">
      <h1>This is an Admin page</h1>
    </div>
    <KnownFaces />
    <AddingUnknownForm />
    <Log />
  </template>