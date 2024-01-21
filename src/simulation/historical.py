from schedule import Schedule
from sim import EloSimulator
from stats import Analyzer

if __name__ == "__main__":
    # data_stop_dates = ["2023/03/01", "2023/05/01", "2023/08/01", "2024/03/01"]
    data_stop_dates = ["2024/03/01"]
    all_games_path = "/home/projects/baseball-MCS/data/intermediate/all_games.json"

    for data_stop_date in data_stop_dates:
        simulator = EloSimulator(k_factor=5, home_advantage=0)
        schedule = Schedule(all_games_path, data_stop_date, simulator)
        n = 1000
        analyzer = Analyzer(n=n)
        analyzer = schedule.sim(analyzer, n=n)
        out = analyzer.export(simulator)
        date = data_stop_date.replace("/", "_")
        out.to_csv(f"/home/projects/baseball-MCS/data/final/{date}probabilities.csv")
