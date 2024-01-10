import React, { useState, useEffect, useContext } from "react";
import { AuthContext } from "./AuthContext";

/////MAIN COMPONENT CODE:
function Generate() {
  const [boardsData, setBoardsData] = useState([]);
  const [riderLevel, setRiderLevel] = useState("");
  const [motorPower, setMotorPower] = useState("");
  const [terrainType, setTerrainType] = useState("");
  const [rangeType, setRangeType] = useState("");

  const [deckType, setDeckType] = useState("");
  const [deckLength, setDeckLength] = useState("");
  const [deckMaterial, setDeckMaterial] = useState("");
  const [truckType, setTruckType] = useState("");
  const [truckWidth, setTruckWidth] = useState("");
  const [controllerFeature, setControllerFeature] = useState("");
  const [controllerType, setControllerType] = useState("");
  const [remoteFeature, setRemoteFeature] = useState("");
  const [remoteType, setRemoteType] = useState("");
  const [motorSize, setMotorSize] = useState("");
  const [motorKv, setMotorKv] = useState("");
  const [wheelSize, setWheelSize] = useState("");
  const [wheelType, setWheelType] = useState("");
  const [batteryVoltage, setBatteryVoltage] = useState("");
  const [batteryType, setBatteryType] = useState("");
  const [batteryCapacity, setBatteryCapacity] = useState("");
  const [batteryConfiguration, setBatteryConfiguration] = useState("");
  const [mileage, setMileage] = useState("");
  const [imageURL, setImageURL] = useState("");

  const { isLoggedIn } = useContext(AuthContext);

  useEffect(() => {
    const updateBoardData = async () => {
      // Post user's input to the Flask backend
      await fetch("/update_board", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          deckType,
          deckLength,
          deckMaterial,
          truckType,
          truckWidth,
          controllerFeature,
          controllerType,
          remoteFeature,
          remoteType,
          motorSize,
          motorKv,
          wheelSize,
          wheelType,
          batteryVoltage,
          batteryType,
          batteryCapacity,
          batteryConfiguration,
          mileage,
          imageURL,
        }),
      });

      // Fetch the latest board
      const response = await fetch("/latest_boards");
      if (response.ok) {
        const latestBoard = await response.json();

        // Set the latest board in the state
        setBoardsData([latestBoard]);
      } else {
        // Handle the case where the latest board is not found
        console.error("Error fetching latest board");
      }
    };

    // Check if any of the relevant state variables have changed
    if (
      deckType !== "" ||
      deckLength !== "" ||
      deckMaterial !== "" ||
      truckType !== "" ||
      truckWidth !== "" ||
      controllerFeature !== "" ||
      controllerType !== "" ||
      remoteFeature !== "" ||
      remoteType !== "" ||
      motorSize !== "" ||
      motorKv !== "" ||
      wheelSize !== "" ||
      wheelType !== "" ||
      batteryVoltage !== "" ||
      batteryType !== "" ||
      batteryCapacity !== "" ||
      batteryConfiguration !== "" ||
      mileage !== "" ||
      imageURL !== ""
    ) {
      // If any of the state variables have changed, update the board data
      updateBoardData();
    }
  }, [
    deckType,
    deckLength,
    deckMaterial,
    truckType,
    truckWidth,
    controllerFeature,
    controllerType,
    remoteFeature,
    remoteType,
    motorSize,
    motorKv,
    wheelSize,
    wheelType,
    batteryVoltage,
    batteryType,
    batteryCapacity,
    batteryConfiguration,
    mileage,
    imageURL,
  ]);

  const handleGenerateBoard = async () => {
    if (!isLoggedIn) {
      alert("Please log in to use the Generate feature.");
      return;
    }

    // Set values for board spec based on user's selection input
    if (riderLevel === "Beginner") {
      setTruckType("Single Kingspin");
      setTruckWidth("10in.");
      setControllerFeature(
        "Low Voltage Cutoff, Overheat Protection, Battery Eliminator Circuit, ABS Braking"
      );
      setControllerType("Flipsky ESC");
      setRemoteFeature("Regen Braking, Reverse, LCD Display");
      setRemoteType("Thumb-Style Throttle");
      setDeckType("Kicktail Cruiser");
      setDeckLength("38in.");
      setDeckMaterial("7-ply plywood");
    } else if (riderLevel === "Intermediate") {
      setTruckType("Double Kingspin");
      setTruckWidth("12in.");
      setControllerFeature(
        "Over-Voltage Protection, 3-12S, BEC, Low-Current Shunt, BLDC Mode, 80A Peak Current"
      );
      setControllerType("VESC 4.6");
      setRemoteFeature(
        "Regen Braking, Reverse, Cruise-Control, LCD Display, Macro Buttons"
      );
      setRemoteType("Trigger-Style Throttle");
      setDeckType("Drop-Through Carver");
      setDeckLength("42in.");
      setDeckMaterial("Carbon Fiber");
    } else if (riderLevel === "Expert") {
      setTruckType("MTB Spring Loaded");
      setTruckWidth("16in.");
      setControllerFeature(
        "Over-Voltage Protection, 3-12S, BEC, Low-Current Shunt, BLDC Mode, FOC Mode, 120A Peak Current, Sensorless Acceleration, Full Torque from 0RPM, Overheat Protection, Aluminum heatsink MOSFET"
      );
      setControllerType("VESC 6.1");
      setRemoteFeature(
        "Regen Braking, Reverse, Cruise Control, LCD Display, Macro Buttons, Ride Mode Toggle"
      );
      setRemoteType("Trigger-Style Throttle");
      setDeckType("35 Degrees MTB Flex");
      setDeckLength("42in.");
      setDeckMaterial("Carbon Fiber 16-Ply");
    }

    if (motorPower === "Drag Racing") {
      setMotorSize("6374");
      setMotorKv("235kv");
    } else if (motorPower === "Casual Cruising") {
      setMotorSize("6356");
      setMotorKv("190kv");
    } else if (motorPower === "Hill Climbing") {
      setMotorSize("6384");
      setMotorKv("170kv");
    }

    if (terrainType === "Street") {
      setWheelSize("90mm");
      setWheelType("78A");
    } else if (terrainType === "All Terrain") {
      setWheelSize("175mm");
      setWheelType("Pneumatic");
    }

    if (rangeType === "Normal") {
      setBatteryVoltage("37v Nominal");
      setBatteryType("18650 li-ion");
      setBatteryCapacity("3500mah per cell");
      setBatteryConfiguration("10s4p");
      setMileage(
        "Approx. 22 miles per charge. Note that mileage will depend on a lot of factors such as: type of wheel, terrain conditions, motor configuration, etc."
      );
    } else if (rangeType === "Extended") {
      setBatteryVoltage("44.4v Nominal");
      setBatteryType("21700 li-ion");
      setBatteryCapacity("4500mah per cell");
      setBatteryConfiguration("12s8p");
      setMileage(
        "Approx. 45 miles per charge. Note that mileage will depend on a lot of factors such as: type of wheel, terrain conditions, motor configuration, etc."
      );
    }
  };

  const renderBoardSpecs = () => (
    <div className="render_board_specs">
      <h2>Build Specs</h2>
      {boardsData.length > 0 ? (
        <ul>
          {boardsData.map((board, index) => (
            <div key={index}>
              <ul className="board_spec">
                <strong className="deck"> Deck </strong>
                <li>Deck Type: {board.deck_type}</li>
                <li>Deck Length: {board.deck_length}</li>
                <li>Deck Material: {board.deck_material}</li>
                <strong className="truck"> Truck </strong>
                <li>Truck Type: {board.truck_type}</li>
                <li>Truck Width: {board.truck_width}</li>
                <strong className="controller"> Controller </strong>
                <li>Controller Feature: {board.controller_feature}</li>
                <li>Controller Type: {board.controller_type}</li>
                <strong className="remote"> Remote </strong>
                <li>Remote Feature: {board.remote_feature}</li>
                <li>Remote Type: {board.remote_type}</li>
                <strong className="motor"> Motor </strong>
                <li>Motor Size: {board.motor_size}</li>
                <li>Motor Kv: {board.motor_kv}</li>
                <strong className="wheel"> Wheel </strong>
                <li>Wheel Size: {board.wheel_size}</li>
                <li>Wheel Type: {board.wheel_type}</li>
                <strong className="battery"> Battery </strong>
                <li>Battery Voltage: {board.battery_voltage}</li>
                <li>Battery Type: {board.battery_type}</li>
                <li>Battery Capacity: {board.battery_capacity}</li>
                <li>Battery Configuration: {board.battery_configuration}</li>
                <strong className="range"> Range </strong>
                <li>Range: {board.range_mileage}</li>
              </ul>
            </div>
          ))}
        </ul>
      ) : (
        <p>
          No build specs available. Click <strong>"Generate Board"</strong> to
          fetch data.
        </p>
      )}
    </div>
  );

  return (
    <div className="generate">
      {isLoggedIn ? (
        <>
          <h2>Build Generator</h2>

          {/* Dropdowns */}
          <label>
            <strong>Rider Level: </strong>
            <select
              value={riderLevel}
              onChange={(e) => setRiderLevel(e.target.value)}
            >
              <option value="">Select Rider Level</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Expert">Expert</option>
            </select>
          </label>
          <br />

          <label>
            <strong>Rider Style: </strong>
            <select
              value={motorPower}
              onChange={(e) => setMotorPower(e.target.value)}
            >
              <option value="">Select Rider Style</option>
              <option value="Drag Racing">Drag Racing</option>
              <option value="Casual Cruising">Casual Cruising</option>
              <option value="Hill Climbing">Hill Climbing</option>
            </select>
          </label>
          <br />

          <label>
            <strong>Terrain Type: </strong>
            <select
              value={terrainType}
              onChange={(e) => setTerrainType(e.target.value)}
            >
              <option value="">Select Terrain Type</option>
              <option value="Street">Street</option>
              <option value="All Terrain">All Terrain</option>
            </select>
          </label>
          <br />

          <label>
            <strong>Range Type: </strong>
            <select
              value={rangeType}
              onChange={(e) => setRangeType(e.target.value)}
            >
              <option value="">Select Range Type</option>
              <option value="Normal">Normal</option>
              <option value="Extended">Extended</option>
            </select>
          </label>
          <br />

          {/* Generate Board Button */}
          <button onClick={handleGenerateBoard}>Generate Board</button>

          {/* Display Board Specs */}
          {renderBoardSpecs()}
        </>
      ) : (
        <p>Please log in to access the Generate feature.</p>
      )}
    </div>
  );
}

export default Generate;
