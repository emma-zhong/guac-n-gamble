'use client';

import { useState } from 'react';
import { Button, Card, Typography, Row, Col } from 'antd';

const { Title, Text } = Typography;

const suits = ['h', 'd', 'c', 's'];
const suitNames = { h: 'Hearts', d: 'Diamonds', c: 'Clubs', s: 'Spades' };
const ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];

const generateCardName = (rank, suit) => `${rank}${suit}.png`;

export default function PokerProbability() {
  const [hand, setHand] = useState([null, null]);
  const [table, setTable] = useState([null, null, null, null, null]);
  const [editingIndex, setEditingIndex] = useState(null);
  const [isEditingTable, setIsEditingTable] = useState(false);
  const [probability, setProbability] = useState(null);

  const selectedCards = new Set([...hand, ...table].filter(Boolean));

  const handleCardSelect = (rank, suit) => {
    const cardName = generateCardName(rank, suit);
    if (selectedCards.has(cardName)) return;

    if (editingIndex !== null) {
      if (isEditingTable) {
        setTable((prevTable) => {
          const newTable = [...prevTable];
          newTable[editingIndex] = cardName;
          return newTable;
        });
      } else {
        setHand((prevHand) => {
          const newHand = [...prevHand];
          newHand[editingIndex] = cardName;
          return newHand;
        });
      }
      setEditingIndex(null);
    }
  };

  const handleCardClick = (index, isTable) => {
    setEditingIndex(index);
    setIsEditingTable(isTable);
  };

  const resetSelection = () => {
    setHand([null, null]);
    setTable([null, null, null, null, null]);
    setProbability(null);
  };

  // const calculateProbability = () => {
  //   setProbability(Math.random().toFixed(4));
  // };
  
  const calculateProbability = async () => {
    const formattedHand = hand.map(card => card?.replace('.png', '')); // Remove .png if it exists
    const formattedTable = table.map(card => card?.replace('.png', ''));
  
    const response = await fetch('http://127.0.0.1:5000/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        hand: formattedHand.filter(Boolean),  // Ensure no nulls
        table: formattedTable.filter(Boolean),
        num_opponents: 2
      })
    });
  
    const data = await response.json();
    setProbability(data.probability ? data.probability.toFixed(2) : "Error");
  };
  

  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: 'auto' }}>
      <Title level={2}>Poker Probability Calculator</Title>

      {/* Hand and Table Cards in One Row */}
      <Row gutter={8} style={{ display: 'flex', justifyContent: 'center', marginBottom: '10px' }}>
        {hand.map((card, index) => (
          <Col key={`hand-${index}`}>
            <Card
              onClick={() => handleCardClick(index, false)}
              style={{
                width: 100,
                height: 140,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                border: '3px solid black',
              }}
            >
              {card ? <img src={`/cards/${card}`} alt={card} width={80} height={120} /> : <Text>Select a Card</Text>}
            </Card>
          </Col>
        ))}
        {table.map((card, index) => (
          <Col key={`table-${index}`}>
            <Card
              onClick={() => handleCardClick(index, true)}
              style={{
                width: 100,
                height: 140,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                backgroundColor: '#f5f5f5',
              }}
            >
              {card ? <img src={`/cards/${card}`} alt={card} width={80} height={120} /> : <Text>Select a Card</Text>}
            </Card>
          </Col>
        ))}
      </Row>

      {/* Card Selection Grid */}
      <Text>Select a Card:</Text>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(13, 1fr)', gap: '5px', marginBottom: '20px' }}>
        {suits.map((suit) =>
          ranks.map((rank) => {
            const cardName = generateCardName(rank, suit);
            return (
              <Card
                key={cardName}
                onClick={() => handleCardSelect(rank, suit)}
                style={{
                  width: 60,
                  height: 90,
                  cursor: selectedCards.has(cardName) ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  opacity: selectedCards.has(cardName) ? 0.5 : 1,
                }}
              >
                <img src={`/cards/${cardName}`} alt={cardName} width={50} height={75} />
              </Card>
            );
          })
        )}
      </div>

      {/* Buttons */}
      <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
        <Button type="primary" onClick={calculateProbability} disabled={hand.includes(null)}>
          Calculate Probability
        </Button>
        <Button type="default" onClick={resetSelection}>
          Reset
        </Button>
      </div>

      {probability !== null && (
        <Card style={{ marginTop: '20px', padding: '10px', textAlign: 'center' }}>
          <Text>Winning Probability: {probability}</Text>
        </Card>
      )}
    </div>
  );
}