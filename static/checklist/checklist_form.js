new Vue({
    el : "#app",
    delimiters : ['[[',']]'],
    data : {
      Items : ["One", "Two", "Three"],
      newCheckbox : "",
      SelectedItems : {
        'One' : "",
        'Two' : "",
        'Three' : "",
      },
      lv_itens:{},
    },
    methods:{
      add:function(){
        Vue.set(this.SelectedItems, this.newCheckbox, false);
        this.Items.push(this.newCheckbox);
      },
      getItem() {
        axios
         .get('http://localhost:5050/item/?format=json')
         .then(response => {
             this.lv_itens = response.data;
             console.log(response.data);

             
         })
         .catch(function (error) {
             console.log(error);
         })
     },
    }
  });