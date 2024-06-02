<template>
  <div class="formularioUsuaraio">
    <form @submit.prevent="submitForm">
      <input type="text" v-model="formData.name" placeholder="Name" />

      <input type="radio" id="male" value="Male" v-model="formData.gender" />

      <label for="male">Male</label>
      <input
        type="radio"
        id="female"
        value="Female"
        v-model="formData.gender"
      />
      <label for="female">Female</label>

      <input
        type="radio"
        id="primary"
        value="Primary"
        v-model="formData.education"
      />
      <label for="primary">Primaria</label>

      <input
        type="radio"
        id="secondary"
        value="Secondary"
        v-model="formData.education"
      />
      <label for="secondary">Secundaria</label>

      <input
        type="radio"
        id="university"
        value="University"
        v-model="formData.education"
      />
      <label for="university">Universidad</label>

      <input
        type="radio"
        id="married"
        value="Married"
        v-model="formData.education"
      />
      <label for="married">Casado/a</label>

      <input
        type="radio"
        id="single"
        value="Single"
        v-model="formData.education"
      />
      <label for="single">Soltero/a</label>

      <input type="number" v-model="formData.salary" placeholder="Salario" />

      <input type="number" v-model="formData.age" placeholder="Edad" />

      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "formUser",
  data() {
    return {
      formData: {
        name: "",
        age: null,
        gender: "",
        salary: null,
        education: "",
        civilStatus: "",
      },
    };
  },
  methods: {
    submitForm() {
      console.log(this.formData);
    },
  },
};
</script>

<style scoped src="../style/formUser.css"></style>
