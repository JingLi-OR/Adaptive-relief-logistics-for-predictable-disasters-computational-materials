# -*- coding: utf-8 -*-
"""
Generation of random spatial instances used in the computational experiments.

The script generates node locations, typhoon trajectories, affected demand points,
population data, and nominal demands. The number of scenarios and periods can be
adjusted through the main block at the end of the file.

Required packages: numpy, pandas, shapely.

Matplotlib is only needed for plotting.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import math
import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon

MILE_TO_KM = 1.609344


@dataclass(frozen=True)
class NetworkConfig:
    """Configuration for generating one synthetic random network."""
    n_mdc: int = 5
    n_sa: int = 10
    n_commodity_suppliers: int = 10
    n_carrier_suppliers: int = 10
    n_demand_points: int = 20
    n_path_points: int = 3
    n_periods: int = 3
    rho: int = 6

    # 72-hour warning window with a 12-hour safety buffer.
    warning_window_hours: int = 60

    # Base seed for one replicate.
    seed: int = 5000


@dataclass(frozen=True)
class Region:
    """A rectangular polygonal region represented by vertices in kilometers."""
    name: str
    vertices: Tuple[Tuple[float, float], ...]

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.vertices)


def _rect_vertices_miles(
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
) -> Tuple[Tuple[float, float], ...]:
    """Return rectangle vertices converted from miles to kilometers."""
    return (
        (x_min * MILE_TO_KM, y_max * MILE_TO_KM),
        (x_max * MILE_TO_KM, y_max * MILE_TO_KM),
        (x_max * MILE_TO_KM, y_min * MILE_TO_KM),
        (x_min * MILE_TO_KM, y_min * MILE_TO_KM),
    )


def default_regions() -> Dict[str, Region]:
    """
    Spatial regions used to generate node locations.

    MDCs are generated in the upstream region:
        [0, 500] x [350, 500] miles.

    SAs, commodity suppliers, carrier suppliers, and DPs are generated in the lower
    service/affected region:
        [0, 500] x [50, 150] miles.
    """
    upstream = _rect_vertices_miles(0, 500, 350, 500)
    lower = _rect_vertices_miles(0, 500, 50, 150)

    return {
        "mdc": Region("MDC", upstream),
        "sa": Region("SA", lower),
        "commodity_supplier": Region("Commodity supplier", lower),
        "carrier_supplier": Region("Carrier supplier", lower),
        "demand_point": Region("Demand point", lower),
    }


def generate_uniform_points_in_polygon(
    vertices: Iterable[Tuple[float, float]],
    n_points: int,
    seed: int,
) -> np.ndarray:
    """Generate random points inside a polygon by rejection sampling."""
    
    rng = np.random.default_rng(seed)
    polygon = Polygon(vertices)
    min_x, min_y, max_x, max_y = polygon.bounds

    points: List[Tuple[float, float]] = []
    while len(points) < n_points:
        candidate = Point(rng.uniform(min_x, max_x), rng.uniform(min_y, max_y))
        if polygon.contains(candidate):
            points.append((candidate.x, candidate.y))

    return np.asarray(points, dtype=float)


def distance_point_to_segment(
    point: Tuple[float, float],
    segment_start: Tuple[float, float],
    segment_end: Tuple[float, float],
) -> float:
    """Compute the Euclidean distance from a point to a line segment."""
    px, py = point
    x1, y1 = segment_start
    x2, y2 = segment_end

    segment_length = math.hypot(x2 - x1, y2 - y1)
    if segment_length == 0:
        return math.hypot(px - x1, py - y1)

    projection = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (segment_length ** 2)
    projection = max(0.0, min(1.0, projection))

    closest_x = x1 + projection * (x2 - x1)
    closest_y = y1 + projection * (y2 - y1)

    return math.hypot(px - closest_x, py - closest_y)


def impact_radius(tau: int) -> float:
    """Return the impact radius r(tau) in kilometers."""
    
    if not (0 <= tau <= 72):
        raise ValueError("tau must be between 0 and 72 hours.")
    return (72 - tau) * 3.154 + 100.0


def n_of_delta(delta_hours: float, rho: int, n_periods: int) -> float:
    """Compute the cumulative affected-population profile N(delta)."""
    
    delta_0 = 12.0 + n_periods * rho / 2.0
    kappa = 2.0 * np.log(19.0) / (n_periods * rho)
    return 1.0 / (1.0 + np.exp(kappa * (delta_hours - delta_0)))


def activation_delay(config: NetworkConfig) -> int:
    """
    Compute the activation delay after warning issuance.

    The warning is issued 72 hours before landfall, and proactive operations stop
    12 hours before landfall for safety. Therefore, the maximum available proactive
    action window is 60 hours. For a planning horizon of n_periods * rho hours:

        tau = 60 - n_periods * rho.
    """
    t_max = int(config.warning_window_hours / config.rho)
    return (t_max - config.n_periods) * config.rho


def delta_by_period(config: NetworkConfig) -> Dict[int, int]:
    """Return the remaining hours before landfall for each period."""
    return {
        t: 12 + (config.n_periods + 1 - t) * config.rho
        for t in range(1, config.n_periods + 2)
    }


def generate_trajectory_scenarios(
    config: NetworkConfig,
) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Generate trajectory candidates from sampled landing and departing points.

    With n_path_points points on each segment, the number of disaster scenarios is
    5 * n_path_points^2.
    """
    rng_landing = np.random.default_rng(config.seed + 101)
    rng_departing = np.random.default_rng(config.seed + 102)

    landing_x = np.sort(
        rng_landing.uniform(0, 500 * MILE_TO_KM, config.n_path_points)
    )
    departing_x = np.sort(
        rng_departing.uniform(0, 500 * MILE_TO_KM, config.n_path_points)
    )

    landing_points = np.column_stack(
        [landing_x, np.zeros(config.n_path_points)]
    )
    departing_points = np.column_stack(
        [departing_x, np.full(config.n_path_points, 150 * MILE_TO_KM)]
    )

    records = []
    trajectory_id = 0
    for i in range(config.n_path_points):
        for j in range(config.n_path_points):
            records.append(
                {
                    "trajectory_id": trajectory_id,
                    "landing_index": i,
                    "departing_index": j,
                    "landing_x": landing_points[i, 0],
                    "landing_y": landing_points[i, 1],
                    "departing_x": departing_points[j, 0],
                    "departing_y": departing_points[j, 1],
                }
            )
            trajectory_id += 1

    return pd.DataFrame(records), landing_points, departing_points


def generate_network(config: NetworkConfig) -> Dict[str, object]:
    """Generate node coordinates and trajectory candidates for one instance."""
    
    regions = default_regions()
    base_seed = config.seed

    mdc_points = generate_uniform_points_in_polygon(
        regions["mdc"].vertices,
        config.n_mdc,
        base_seed + 11,
    )

    sa_points = generate_uniform_points_in_polygon(
        regions["sa"].vertices,
        config.n_sa,
        base_seed + 21,
    )

    commodity_supplier_points = generate_uniform_points_in_polygon(
        regions["commodity_supplier"].vertices,
        config.n_commodity_suppliers,
        base_seed + 31,
    )

    carrier_supplier_points = generate_uniform_points_in_polygon(
        regions["carrier_supplier"].vertices,
        config.n_carrier_suppliers,
        base_seed + 41,
    )

    demand_points = generate_uniform_points_in_polygon(
        regions["demand_point"].vertices,
        config.n_demand_points,
        base_seed + 51,
    )

    trajectories, landing_points, departing_points = generate_trajectory_scenarios(config)

    return {
        "config": config,
        "regions": regions,
        "mdc_points": mdc_points,
        "sa_points": sa_points,
        "commodity_supplier_points": commodity_supplier_points,
        "carrier_supplier_points": carrier_supplier_points,
        "demand_points": demand_points,
        "trajectories": trajectories,
        "landing_points": landing_points,
        "departing_points": departing_points,
        "n_trajectory_scenarios": config.n_path_points * config.n_path_points,
        "n_disaster_scenarios": 5 * config.n_path_points * config.n_path_points,
    }


def identify_affected_demand_points(
    network: Dict[str, object],
    tau: int | None = None,
) -> pd.DataFrame:
    """
    Identify affected demand points for each trajectory scenario.

    A demand point is affected if its perpendicular distance to the trajectory line
    segment is less than r(tau).
    """
    config: NetworkConfig = network["config"]
    if tau is None:
        tau = activation_delay(config)

    radius = impact_radius(tau)
    demand_points = network["demand_points"]
    trajectories: pd.DataFrame = network["trajectories"]

    records = []
    for row in trajectories.itertuples(index=False):
        start = (row.landing_x, row.landing_y)
        end = (row.departing_x, row.departing_y)

        for demand_point_id, point in enumerate(demand_points):
            distance = distance_point_to_segment(tuple(point), start, end)
            if distance < radius:
                records.append(
                    {
                        "trajectory_id": int(row.trajectory_id),
                        "demand_point_id": demand_point_id,
                        "distance_to_trajectory": distance,
                        "impact_radius": radius,
                        "tau": tau,
                    }
                )

    return pd.DataFrame(
        records,
        columns=[
            "trajectory_id",
            "demand_point_id",
            "distance_to_trajectory",
            "impact_radius",
            "tau",
        ],
    )


def generate_population_and_nominal_demand(
    network: Dict[str, object],
    tau: int | None = None,
    intensity_rates: Tuple[float, ...] = (0.025, 0.050, 0.075, 0.125, 0.250),
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate DP population data and nominal demand for affected DP-scenario-period records.

    The vulnerable population is 10% of the generated total population. Nominal
    demand equals 9 times the newly affected population.
    """
    config: NetworkConfig = network["config"]
    if tau is None:
        tau = activation_delay(config)

    rng = np.random.default_rng(config.seed + 201)
    total_population = rng.integers(
        low=5000,
        high=50000,
        size=config.n_demand_points,
    ) * 10
    sensitive_population = (total_population * 0.1).astype(int)

    population_df = pd.DataFrame(
        {
            "demand_point_id": range(config.n_demand_points),
            "total_population": total_population,
            "sensitive_population": sensitive_population,
        }
    )

    affected = identify_affected_demand_points(network, tau=tau)
    affected_pairs = set(zip(affected["trajectory_id"], affected["demand_point_id"]))

    deltas = delta_by_period(config)
    n_t = {
        t: n_of_delta(deltas[t], config.rho, config.n_periods)
        for t in range(1, config.n_periods + 2)
    }
    denominator = n_t[config.n_periods + 1] - n_t[1]

    if abs(denominator) < 1e-12:
        raise ValueError("Invalid demand time profile: denominator is zero.")

    n_tracks = config.n_path_points * config.n_path_points

    records = []
    for trajectory_id in range(n_tracks):
        for demand_point_id in range(config.n_demand_points):
            if (trajectory_id, demand_point_id) not in affected_pairs:
                continue

            for level, rate in enumerate(intensity_rates):
                disaster_scenario_id = trajectory_id + level * n_tracks

                for t in range(1, config.n_periods + 1):
                    period_share = (n_t[t + 1] - n_t[t]) / denominator
                    newly_affected_population = round(
                        sensitive_population[demand_point_id] * rate * period_share
                    )
                    nominal_demand = 9 * newly_affected_population

                    records.append(
                        {
                            "disaster_scenario_id": disaster_scenario_id,
                            "trajectory_id": trajectory_id,
                            "intensity_level": level + 1,
                            "intensity_rate": rate,
                            "demand_point_id": demand_point_id,
                            "period": t,
                            "delta_hours": deltas[t],
                            "newly_affected_population": newly_affected_population,
                            "nominal_demand": nominal_demand,
                        }
                    )

    nominal_demand_df = pd.DataFrame(
        records,
        columns=[
            "disaster_scenario_id",
            "trajectory_id",
            "intensity_level",
            "intensity_rate",
            "demand_point_id",
            "period",
            "delta_hours",
            "newly_affected_population",
            "nominal_demand",
        ],
    )

    return population_df, nominal_demand_df


def points_to_dataframe(points: np.ndarray, node_type: str) -> pd.DataFrame:
    """Convert point coordinates to a DataFrame."""
    return pd.DataFrame(
        {
            "node_type": node_type,
            "node_id": range(len(points)),
            "x_km": points[:, 0],
            "y_km": points[:, 1],
        }
    )


def export_network(
    network: Dict[str, object],
    output_dir: str | Path,
    tau: int | None = None,
) -> None:
    """
    Export node coordinates, trajectories, affected DPs, population data, and nominal demand.
    """
    config: NetworkConfig = network["config"]
    if tau is None:
        tau = activation_delay(config)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    node_frames = [
        points_to_dataframe(network["mdc_points"], "MDC"),
        points_to_dataframe(network["sa_points"], "SA"),
        points_to_dataframe(network["commodity_supplier_points"], "commodity_supplier"),
        points_to_dataframe(network["carrier_supplier_points"], "carrier_supplier"),
        points_to_dataframe(network["demand_points"], "demand_point"),
    ]
    pd.concat(node_frames, ignore_index=True).to_csv(
        output_path / "node_coordinates.csv",
        index=False,
    )

    network["trajectories"].to_csv(
        output_path / "trajectory_scenarios.csv",
        index=False,
    )

    identify_affected_demand_points(network, tau=tau).to_csv(
        output_path / f"affected_demand_points_tau_{tau}.csv",
        index=False,
    )

    population_df, nominal_demand_df = generate_population_and_nominal_demand(
        network,
        tau=tau,
    )
    population_df.to_csv(
        output_path / "demand_point_population.csv",
        index=False,
    )
    nominal_demand_df.to_csv(
        output_path / "nominal_demand.csv",
        index=False,
    )

    pd.DataFrame(
        {
            "parameter": [
                "n_mdc",
                "n_sa",
                "n_commodity_suppliers",
                "n_carrier_suppliers",
                "n_demand_points",
                "n_path_points",
                "n_periods",
                "rho",
                "warning_window_hours",
                "tau",
                "impact_radius",
                "seed",
                "mdc_seed",
                "sa_seed",
                "commodity_supplier_seed",
                "carrier_supplier_seed",
                "demand_point_seed",
                "landing_point_seed",
                "departing_point_seed",
                "population_seed",
                "n_trajectory_scenarios",
                "n_disaster_scenarios",
            ],
            "value": [
                config.n_mdc,
                config.n_sa,
                config.n_commodity_suppliers,
                config.n_carrier_suppliers,
                config.n_demand_points,
                config.n_path_points,
                config.n_periods,
                config.rho,
                config.warning_window_hours,
                tau,
                impact_radius(tau),
                config.seed,
                config.seed + 11,
                config.seed + 21,
                config.seed + 31,
                config.seed + 41,
                config.seed + 51,
                config.seed + 101,
                config.seed + 102,
                config.seed + 201,
                network["n_trajectory_scenarios"],
                network["n_disaster_scenarios"],
            ],
        }
    ).to_csv(output_path / "generation_settings.csv", index=False)


def plot_network(
    network: Dict[str, object],
    save_path: str | Path | None = None,
    show: bool = True,
) -> None:
    """Plot node locations and trajectory line segments in miles."""
    import matplotlib.pyplot as plt

    regions: Dict[str, Region] = network["regions"]
    style = {
        "mdc": ("red", "o", "MDC"),
        "sa": ("blue", "s", "SA"),
        "commodity_supplier": ("purple", "D", "Commodity supplier"),
        "carrier_supplier": ("orange", "*", "Carrier supplier"),
        "demand_point": ("green", "+", "Demand point"),
    }
    point_keys = {
        "mdc": "mdc_points",
        "sa": "sa_points",
        "commodity_supplier": "commodity_supplier_points",
        "carrier_supplier": "carrier_supplier_points",
        "demand_point": "demand_points",
    }

    plt.figure(figsize=(12, 12))

    for region_key, (color, marker, label) in style.items():
        vertices = np.asarray(regions[region_key].vertices) / MILE_TO_KM
        plt.plot(
            np.append(vertices[:, 0], vertices[0, 0]),
            np.append(vertices[:, 1], vertices[0, 1]),
            color=color,
            label=f"{label} region",
        )

        points = network[point_keys[region_key]] / MILE_TO_KM
        plt.scatter(
            points[:, 0],
            points[:, 1],
            color=color,
            marker=marker,
            s=15,
            label=f"{label} points",
        )

    trajectories = network["trajectories"]
    for row in trajectories.itertuples(index=False):
        plt.plot(
            [row.landing_x / MILE_TO_KM, row.departing_x / MILE_TO_KM],
            [row.landing_y / MILE_TO_KM, row.departing_y / MILE_TO_KM],
            color="gray",
            linestyle="--",
            linewidth=0.5,
        )

    landing_points = network["landing_points"] / MILE_TO_KM
    departing_points = network["departing_points"] / MILE_TO_KM

    plt.scatter(
        landing_points[:, 0],
        landing_points[:, 1],
        color="cyan",
        marker="<",
        label="Landing points",
    )
    plt.scatter(
        departing_points[:, 0],
        departing_points[:, 1],
        color="magenta",
        marker=">",
        label="Departing points",
    )

    config: NetworkConfig = network["config"]
    plt.title(
        f"Synthetic relief logistics network "
        f"(seed={config.seed}, |S|={network['n_disaster_scenarios']})"
    )
    plt.xlabel("x-coordinate (miles)")
    plt.ylabel("y-coordinate (miles)")

    plt.xlim(0, 500)
    plt.ylim(0, 500)
    plt.gca().set_aspect("equal", adjustable="box")

    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


if __name__ == "__main__":

    seeds = [5000, 6000, 7000, 8000, 9000]
    
    # To change the instance size, adjust n_path_points and n_periods.
    # The number of disaster scenarios is 5 * n_path_points^2.
    for rep_id, seed in enumerate(seeds, start=1):
        config = NetworkConfig(
            n_mdc=5,
            n_sa=10,
            n_commodity_suppliers=10,
            n_carrier_suppliers=10,
            n_demand_points=20,
            n_path_points=3,
            n_periods=3,
            rho=6,
            warning_window_hours=60,
            seed=seed,
        )

        network = generate_network(config)
        tau = activation_delay(config)

        output_dir = Path(f"generated_instances/instance_rep_{rep_id}_seed_{seed}")
        export_network(network, output_dir=output_dir, tau=tau)

        # Optional plot.
        figure_path = output_dir / f"network_rep_{rep_id}_seed_{seed}.png"
        plot_network(network, save_path=figure_path, show=False)

        print(f"Generated: {output_dir}")
        print(f"  Figure saved to: {figure_path}")
        print(f"  Activation delay tau = {tau} hours")
        print(f"  Impact radius r(tau) = {impact_radius(tau):.3f} km")
        print(f"  Number of disaster scenarios = {network['n_disaster_scenarios']}")
