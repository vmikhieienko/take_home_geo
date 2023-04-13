# Take Home Task

## How to run
1. `docker-compose -f deployment/docker-compose.local.yaml --env-file deployment/.env.example up -d`
2. Open: http://localhost:8000/graphql
3. JFYI: the mock vehicles data are loaded to DB via migrations for convenience
4. All secrets are stored or hardcoded for the convenience, NEVER store secrets in VCS.

## 1. API Calls:
- Create shifts:
```graphql
 mutation createShiftManual {
    createShiftManual {
        shift {
            id
        }
    }
}
```

- Add vehicles to shifts (Idempotent):
```graphql
mutation addVehiclesToShift ($shift_id: ID!, $vehicle_ids: [ID]!) {
    addVehiclesToShift (args: {shiftId: $shift_id, vehicleIds: $vehicle_ids}) {
        shift {
            id
            vehicles {
                id
            }
        }
    }
}
```

- Complete a battery swap for a vehicle:
```graphql
mutation completeSwap ($shift_id: ID!, $vehicle_id: ID!) {
    completeSwap (args: {shiftId: $shift_id, vehicleId: $vehicle_id}) {
        swap {
            id
            completed
            vehicle {
                id
                batteryLevel
            }
        }
    }
}
```

- Check if a swap has been completed for any vehicle in a shift:
```graphql
query swap ($shift_id: ID!, $vehicle_id: ID!) {
    swap (shiftId: $shift_id, vehicleId: $vehicle_id){
        id
        completed
        vehicle {
            id
            licensePlate
        }
    }
}
```

- Query shift to see if all vehicles in the shift have had their battery swaps + review all vehicles in a shift:
```graphql
query shift ($shift_id: ID!) {
    shift (shiftId: $shift_id){
        id
        swaps {
            id
            completed,
            vehicle {
                id
                licensePlate
            }
        }
        vehicles {
            id
            licensePlate
            batteryLevel
        }
    }
}
```


## 2. Auto Shift Creation
```graphql
mutation createShiftAuto($lat: Float!, $lon: Float!) {
    createShiftAuto (args: {lat: $lat, lon: $lon}) {
        shift {
            id
            vehicles {
                id
                batteryLevel
                location {
                    type
                    coordinates
                }
            }
        }
    }
}
```



### Idea
The most accurate result to build the optimal vehicles order and reduce driving distance using bruteforce will take `O(n!)`
in the worst case which is not an option in real-time application with the provided parameter of `20`.

That is why used an [approximation algorithm](https://iq.opengenus.org/approximation-algorithm-for-travelling-salesman-problem/)
(Prim's MST + DFS) for the traveling salesman problem to get a better performance of `O(n^2)`.


### Storing in DB
The swaps are created in ascending order so the first point has the lowest id, the last point has the biggest id.


## Testing

To test locally make sure you installed `gdal` and run:

```bash
cd backend && ./manage.py test
```

To test inside the image, change the running command to:

```yaml
command: ./manage.py test
```