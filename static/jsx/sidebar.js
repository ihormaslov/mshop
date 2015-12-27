var CategoriesBox = React.createClass({
    loadCommentsFromServer: function(){
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data});
                console.log('asdfasdfasdf')
            }.bind(this),
            error: function(xhr, status, err) {
                console.log('123123123')
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    getInitialState: function(){
        return {data: []};
    },
    componentDidMount: function(){
        // this.loadCommentsFromServer();
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    render: function(){
        return(
            <ul className="react-sidebar">
                <CategoriesList data={this.state.data} />
            </ul>
        );
    }
});

var CategoriesList = React.createClass({
    render: function(){
        var categoryNodes = this.props.data.map(function(item){
            return(
                <Category>
                    {item.name}
                </Category>
            )
        }),
        return(

        )
    }
})

var Category = React.createClass({
    render: function (){
        return(
            <li>{this.props.name}</li>
        )
    }
})

ReactDOM.render(
    <CategoriesList url="/api/categories/" />,
    document.getElementById('react-sidebar')
);

