import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def main():
    df = px.data.iris()

    # Split data into training and test splits
    train_idx, test_idx = train_test_split(df.index, test_size=0.25, random_state=0)
    df["split"] = "train"
    df.loc[test_idx, "split"] = "test"

    X = df[["sepal_width", "sepal_length"]]
    y = df["petal_width"]
    X_train = df.loc[train_idx, ["sepal_width", "sepal_length"]]
    y_train = df.loc[train_idx, "petal_width"]

    # Condition the model on sepal width and length, predict the petal width
    model = LinearRegression()
    model.fit(X_train, y_train)
    df["prediction"] = model.predict(X)

    fig = px.scatter(
        df,
        x="petal_width",
        y="prediction",
        marginal_x="histogram",
        marginal_y="histogram",
        color="split",
        trendline="ols",
    )
    fig.update_traces(histnorm="probability", selector={"type": "histogram"})
    fig.add_shape(
        type="line",
        line=dict(dash="dash"),
        x0=y.min(),
        y0=y.min(),
        x1=y.max(),
        y1=y.max(),
    )

    return fig
