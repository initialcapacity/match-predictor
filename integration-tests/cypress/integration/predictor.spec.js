describe('match predictor', () => {
    it('compare two teams', () => {
        cy.visit('http://localhost:3010');

        cy.contains('Match Predictor').should('exist');

        cy.get('#home-league').select('italy 1')
        cy.get('#home-team').select('Always Wins')

        cy.get('#away-league').select('italy 1')
        cy.get('#away-team').select('Always Loses')

        cy.contains('Submit').click()

        cy.contains('HOME').should('exist')
        cy.contains('100%').should('exist')
    });
});
