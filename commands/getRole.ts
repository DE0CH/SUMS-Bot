import { SlashCommandBuilder, Interaction } from 'discord.js';

export const data = new SlashCommandBuilder().setName('ping').setDescription('Replies with Pong!')
export function execute(interaction: Interaction) {
  
}