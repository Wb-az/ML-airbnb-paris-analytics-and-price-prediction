import os
import joblib
from collections import defaultdict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler

# Models
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor  # VotingRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from skorch import NeuralNetRegressor
import torch
from torch import nn
from tqdm import tqdm
# metrics
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, r2_score


models_dir = os.path.join(os.getcwd(), 'models')
try:
    os.mkdir(models_dir)
except FileExistsError:
    pass


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class PriceRegressor(nn.Module):
    def __init__(self, inputs=None, hidden=None, p=0.2):
        super(PriceRegressor, self).__init__()

        assert len(hidden) == 3, 'hidden must be a list containing three sizes'

        self.input = inputs
        self.hidden = hidden
        self.dropout = nn.Dropout(p)

        self.regressor = nn.Sequential(
            nn.Linear(self.input, self.hidden[0]),
            nn.ReLU(),
            nn.Dropout(p),
            nn.Linear(self.hidden[0], self.hidden[1]),
            nn.ReLU(),
            nn.Dropout(p),
            nn.Linear(self.hidden[1], self.hidden[2]),
            nn.ReLU(),
            nn.Linear(self.hidden[2], 1))

    def forward(self, x):

        x = x.type('torch.FloatTensor').to(device)
        out = self.regressor(x)

        return out


def get_models(percentile_index):
    common_params = dict(random_state=123, learning_rate=0.05, max_depth=10,
                         min_samples_leaf=20)
    models = dict()

    # Linear Models
    models['linear_regression'] = LinearRegression()
    models['lasso'] = Lasso(max_iter=1500)
    models['ridge'] = Ridge()

    # Support Vector Machines
    models['svr'] = SVR(C=5, cache_size=500, epsilon=0.2)

    # Decision trees
    models['decision_tree'] = DecisionTreeRegressor(max_depth=10, random_state=123)

    # Ensemble methods
    models['random_forrest'] = RandomForestRegressor(random_state=123, n_estimators=300,
                                                     max_depth=10, min_samples_leaf=20)
    models['gradient_boosting'] = GradientBoostingRegressor(**common_params, n_estimators=300)
    models['hist_gradient_boosting'] = HistGradientBoostingRegressor(**common_params,
                                                                     l2_regularization=0.001)
    models['xgb'] = XGBRegressor(objective='reg:squarederror', learning_rate=0.05,
                                 max_depth=10, n_estimators=500, tree_methd='gpu_exact',
                                 n_gpus=1, predictor='gpu_predictor',
                                 alpha=0.001, max_leaves=2, verbosity=0)
    models['LGBM'] = LGBMRegressor(learning_rate=0.05, max_depth=10,
                                   n_estimators=500, alpha=0.001, max_leaves=2)

    # Shallow neural network
    models['ann_regressor'] = NeuralNetRegressor(module=PriceRegressor,
                                                 module__input=len(percentile_index),
                                                 module__hidden=[512, 512, 256],
                                                 module__p=0.3,
                                                 train_split=None,
                                                 max_epochs=300,
                                                 optimizer=torch.optim.AdamW,
                                                 lr=0.001,
                                                 device=device,
                                                 iterator_train__shuffle=True,
                                                 verbose=0)

    return models


def ann_datasets(x, y):

    return x.values, y.values.reshape(-1, 1)


def evaluation(x, y, model):
    y_pred = model.predict(x)
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_percentage_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = mean_squared_error(y, y_pred, squared=False)

    return r2, mae, mse, rmse, y_pred


def train_models(train, val, test, model_dir=None, best_features=None, robust_scaler=False,
                 save=False):
    metrics = defaultdict(dict)
    models = get_models(percentile_index=best_features)

    x_train, y_train = train[0][best_features], train[1]
    x_val, y_val = val[0][best_features], val[1]
    x_test, y_test = test[0][best_features], test[1]

    for k, v in tqdm(models.items()):

        print(f'Buiding {k} pipeline')

        if robust_scaler:
            pipe = make_pipeline(RobustScaler(), v)
        else:
            pipe = make_pipeline(StandardScaler(), v)

        if k == 'ann_regressor':

            x_train, y_train = ann_datasets(x_train, y_train)
            x_val, y_val = ann_datasets(x_val, y_val)
            x_test, y_test = ann_datasets(x_test, y_test)

        model = pipe.fit(x_train, y_train)
        r2 = model.score(x_train, y_train)

        # Validation
        v_r2, v_mae, v_mse, v_rmse, v_pred = evaluation(x_val, y_val, model)

        # Test
        t_r2, t_mae, t_mse, t_rmse, t_pred = evaluation(x_test, y_test, model)

        if save:
            filename = os.path.join(model_dir, f'{k}.sav')
            joblib.dump(model, filename)

        metrics[k] = {'train_r2': r2, 'val_r2': v_r2, 'test_r2': t_r2,
                      'mean_yhat_val': v_pred.mean(), 'mean_yhat_test': t_pred.mean(),
                      'val_mae': v_mae, 'test_mae': t_mae, 'val_mse': v_mse,
                      'test_mse': t_mse, 'val_rmse': v_rmse, 'test_rmse': t_rmse}

    return metrics


# get_depth()
# get_n_leaves()
# score(X, y, sample_weight=None)

# import graphviz
# from sklearn.tree import export_graphviz
#
# dot_data = export_graphviz(tree, out_file=None)
# graph = graphviz.Source(dot_data)