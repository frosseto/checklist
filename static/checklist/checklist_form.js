function alerta(data) {
  if (!isEmpty(data.alert_text)){
    let classe = ""
    $('#tile-alert').removeClass();
    $('#alert-strong-text').text(data.alert_title + ": ")
    $('#alert-text').text(data.alert_text)
    switch(data.alert_type){
      case 'erro':
        classe = "alert alert-danger alert-fixed"
        break;
      case 'sucesso':
        classe = "alert alert-success alert-fixed"
        break;
      default:
        classe = "alert alert-warning alert-fixed"
    }
    $('#tile-alert').addClass(classe);
    $('#tile-alert').fadeIn(1000);
    setTimeout(function() { 
        $('#tile-alert').fadeOut(1000); 
    }, 3000);
  };
};



function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}



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
    edit: false,
    create: false,
    lv_itens : {},
    lv_selected_itens: {},
    grupo_acesso: '',
    lv: {
         id: '',
         modelo:'',
         nome:'',
         observacao:'',
         status:'Em elaboração',
        },
  },
  computed: {

    lv_itens_grouped: function(){
      return groupBy(this.lv_itens, 'grupo')
    },

    isDisabled() {
      if (this.grupo_acesso=='Executante' && this.lv['status']=='Em elaboração'){
        return !(this.create || this.edit);
      }
      else{
        return true;
      }
    },

    isDisabledObs() {
      if (  (this.grupo_acesso=='Executante' && this.lv['status']=='Em elaboração') ||
            (this.grupo_acesso=='Aprovador' && this.lv['status']=='Aguardando Aprovador')  ){
        return !(this.create || this.edit);
      } else {
        return true;
      }
    },


  },
    methods:{

      goBack() {
        window.history.back();
      },

      getLV() {

        this.lv['modelo']=modelo_pk;
        this.lv['id']=lv_pk;

        axios({
          method:'get',
          url: 'item/?format=json&modelo=' + modelo_pk,
          baseURL: '/',
          })
          .then(response => {
            lv_itens = response.data;
            this.lv_itens = lv_itens;

            // valores padrao
            if (lv_pk==''){
              console.log('inicializar com valores padrao')

              var lv_selected_itens = {};
              var itens = this.lv_itens;        
              itens.forEach(item => {
                id = item['id']
                respostapadrao = item['valorpadrao']
                console.log('id '+id+' respostapadrao '+respostapadrao)
                if ( !isEmpty(respostapadrao)){
                  lv_selected_itens[id]=respostapadrao
                }
              });
              this.lv_selected_itens=lv_selected_itens;


              }

          })
          .catch(function (error) {
              console.log(error);
        });


        if (!isEmpty(lv_pk)){

          axios({
            method:'get',
            url: 'listaverificacao/' + lv_pk + '/?format=json',
            baseURL: '/',
          })
          .then(response => {
              lv = response.data;
              console.log(response.data);
              this.lv['nome']=lv['nome']
              this.lv['observacao']=lv['observacao']
              this.lv['status']=lv['status']
          })
          .catch(function (error) {
              console.log(error);
          });

          axios({
            method:'get',
            url: 'listaverificacaoxitemxresposta/?format=json&listaverificacao=' + lv_pk,
            baseURL: '/',
          })
          .then(response => {
              console.log('respostas')
              selected_itens = response.data
              console.log(selected_itens)

              var lv_selected_itens = {};
              selected_itens.forEach(item=>{
                var resposta = ""
                if (['True', 'False'].includes(item.resposta)){
                  resposta = (item.resposta === 'True');
                } else {
                  resposta = item.resposta;
                }  
                lv_selected_itens[item.item]=resposta;
                console.log('resposta: ' + item.item + ' ' + '; reposta: ' + resposta + ' ' + lv_selected_itens[item.item])
              })

              this.lv_selected_itens=lv_selected_itens;
          })
          .catch(function (error) {
              console.log(error);
          });
        } 
      },

      updateID(id){
        if (this.lv['id']==''){
          this.lv['id']=id
        };
      },


      saveLV(){
        
        data = {
          'lv': JSON.stringify(this.lv),
          'lv_selected_itens': JSON.stringify(this.lv_selected_itens)
        }

        if(this.lv['id']==''){
          url=''        
          msg = {alert_text: 'LV criada', alert_title: 'Aviso'}
          this.create=false
        }
        else{
          url = '/checklist/' + this.lv['id'] + '/save/'
          msg = {alert_text: 'LV atualizada', alert_title: 'Aviso'}
        }

        const csrftoken = getCookie('csrftoken');
        console.log(csrftoken)
        console.log(data)
        $.ajax({
            url: url,
            data: data,
            type: 'POST',
            dataType: 'json',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
              },
            success: data => {
                console.log(data.lv_pk)
                this.updateID(data.lv_pk)
                alerta(msg)
          }
        });
        this.edit=false;
      },

      editLV(event){
          targetId = event.currentTarget.id;
          console.log(targetId);
          this.edit = !this.edit;
      },

      acaoLV(event){
        targetId = event.currentTarget.id;
        acao_status = {'retornar-lv':'Em elaboração',
                       'enviar-aprovacao-lv': 'Aguardando Aprovador',
                       'aprovar-lv': 'Aprovada',
                      };
        this.lv['status']= acao_status[targetId]
        console.log(this.lv['status'])
        this.saveLV();
      },

      deleteLV(){
        console.log('Delete LV')
        url = '/checklist/' + this.lv['id'] + '/delete/'
        const csrftoken = getCookie('csrftoken');
        console.log(csrftoken)
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
              },
            success: data => {
                console.log(data['msg'])
                window.location.href = '/checklist_pesquisa';
          }
        });
      },


  },
  created: function(){
    this.grupo_acesso=grupo_acesso.text.replace(/"/g,"");;
    this.create=lv_pk==='';
    this.getLV()
}
})