

function groupBy(array, key){
    const result = {}
    // verifica se array existe e se tem pelo menos 1 item
    if (typeof array !== 'undefined' && array.length > 0) {
      array.forEach(item => {
        if (!result[item[key]]){
          result[item[key]] = []
        }
        result[item[key]].push(item)
      })
    }
    return result
  };


var vm = new Vue({
  el: '#app',
  delimiters : ['[[',']]'],
  data: {
    lv_itens : {},
    lv_selected_itens: {},
    lv: {},
  },
  computed: {
    // uma função "getter" computada (computed getter)
    reversedMessage: function (){
      // `this` aponta para a instância Vue da variável `vm`
      return this.message.split('').reverse().join('')
    },

    lv_itens_grouped: function(){
      return groupBy(this.lv_itens, 'grupo')
    },

  },
    methods:{
      getLV() {
      axios
        .get('http://localhost:5000/item/?format=json&modelo=' + modelo)
        .then(response => {
            this.lv_itens = response.data;
            console.log(response.data);
        })
        .catch(function (error) {
            console.log(error);
        })
    },
  },
  created: function(){
    this.getLV()
}
})