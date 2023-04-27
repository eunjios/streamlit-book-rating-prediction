import torch

from model import FieldAwareFactorizationMachineModel

def model_load(data) -> FieldAwareFactorizationMachineModel:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = FieldAwareFactorizationMachineModel(embed_dim=16, data=data).to(device)
    return model


def modify_range(x):
    if x < 0:
        return 1
    elif x > 10:
        return 10
    else:
        return x

def test(model, dataloader):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    predicts = list()
    model.load_state_dict(torch.load('saved_model/FFM_model.pt', map_location=device))
    # if args.use_best_model == True:
    #     model.load_state_dict(torch.load('saved_model/FFM_model.pt'))
    # else:
    #     pass
    model.eval()

    for _, data in enumerate(dataloader['test_dataloader']):
        x = data[0].to(device)
        y_hat = model(x)
        list_ = y_hat.tolist()
        list_ = list(map(modify_range , list_))
        predicts.extend(list_)
    return predicts

def test_(model, data, id, isbn):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    predicts = list()
    model.load_state_dict(torch.load('saved_model/FFM_model.pt', map_location=device))
    model.eval()

    mask = (data['test']['user_id'] == id) & (data['test']['isbn'] == isbn)
    x = data['test'][mask].to(device)
    y_hat = model(x)
    return round(y_hat, 2)
    for _, data in enumerate(dataloader['test_dataloader']):
        x = data[0].to(device)
        y_hat = model(x)
        list_ = y_hat.tolist()
        list_ = list(map(modify_range , list_))
        predicts.extend(list_)
    return predicts